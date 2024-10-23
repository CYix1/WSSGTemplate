using System.Collections.Generic;
using Core.Websocket;
using MISC;
using Newtonsoft.Json;
using ServerClasses;
using TMPro;
using UnityEngine;
using WebSocketSharp;

namespace Examples.TicTacToe.Websocket
{
    /*
     * The websocket variant for TTT Lobby
     */
    public class TTTLobbyCommunicationWS : CommunicationWS
    {
        [Header("Lobby References")] public TextMeshProUGUI lobbyNameLabel;

        public TMP_InputField opponentInputField;
        public TextMeshProUGUI informationLabel;
        public GameObject gamePanel;
        public Popup popup;


        private ServerLobby currentLobby;

        //new variables needed to delay the UI updating
        //The UI cannot be updated outside of the main thread
        private ServerMessage lastServerMessage;
        private string lobbyID;
        private string opponentName;
        private bool showMessage;

        private void Update()
        {
            /*
             * UI, GameObject updates cannot be on an other thread...
             */

            if (showMessage)
            {
                showMessage = false;
                popup.SetMessage(lastServerMessage);
            }

            if (currentLobby != null)
                if (currentLobby.players.Count == 2)
                    GoToGamePanel();
        }

        public void ResetLobby()
        {
            currentLobby = null;
        }

        public void GoToGamePanel()
        {
            if (currentLobby == null)
                return;

            StartLobby();
            gameObject.SetActive(!gameObject.activeSelf);
            gamePanel.SetActive(!gamePanel.activeSelf);
            var game = gamePanel.GetComponent<TTTGameCommunicationWS>();
            game.init(currentLobby);
            ws.CloseAsync();
        }

        //this method is the "WS variant" for the whole timer update thing
        public override void WsOnOnMessage(object sender, MessageEventArgs e)
        {
            //handle responses
            var serverMessage = JsonConvert.DeserializeObject<ServerMessage>(e.Data);

            if (serverMessage.IsShowMessage())
                showMessage = true; //delay update of UI

            if (serverMessage.IsData())
                //one if needed, just to prepare for the future 
                switch (serverMessage.extraMessage)
                {
                    case "lobbyData":
                        currentLobby = JsonConvert.DeserializeObject<ServerLobby>(serverMessage.message);
                        break;
                }

            lastServerMessage = serverMessage;
        }

        #region ServerCalls

        public void CreateLobby()
        {
            lobbyID = opponentInputField.text;
            url = "TTT/" + lobbyID;

            var dataToSend = new Dictionary<string, object>
            {
                { "id", lobbyID },
                { "host", TemplateSettings.username }
            };
            //sending it via websockets.
            SendMessageAsync(GenerateServerMessage(dataToSend, "CREATE LOBBY"));
        }

        public void DebugServerCall()
        {
            url = "TTT/debug";

            //sending it via websockets.
            SendMessageAsync(GenerateServerMessage(null, "DEBUG"));
        }


        public void JoinLobby()
        {
            url = "TTT/" + opponentInputField.text;
            var dataToSend = new Dictionary<string, object>
            {
                { "lobbyId", opponentInputField.text },
                { "id", TemplateSettings.username }
            };
            //sending it via websockets.
            SendMessageAsync(GenerateServerMessage(dataToSend, "JOIN LOBBY"));
        }

        public void StartLobby()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", lobbyID },
                { "startGame", "True" } //python variant of true, false
            };

            //sending it via websockets.
            SendMessageAsync(GenerateServerMessage(dataToSend, "START LOBBY"));
        }

        #endregion
    }
}