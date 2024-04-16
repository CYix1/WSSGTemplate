using System.Collections.Generic;
using Newtonsoft.Json;
using ServerClasses;
using TMPro;
using UnityEngine;
using WebSocketSharp;

namespace BasicRest
{
    /*
     * Script which handles the Lobby stuff in Scenes/Examples/REST/TicTacToeRest
     */
    public class TTTLobbyRest : MonoBehaviour
    {
        [Header("References")] public TextMeshProUGUI lobbyNameLabel;

        public TMP_InputField opponentInputField;
        public TextMeshProUGUI informationLabel;
        public GameObject gamePanel;
        public Popup popup;


        private ServerLobby currentLobby;
        private string lobbyID;
        private string opponentName;

        private void Start()
        {
            lobbyNameLabel.text = TemplateSettings.username;
        }

        public void ResetLobby()
        {
            currentLobby = null;
        }

        //init and set a bool value in the database 
        public void GoToGamePanel(ServerLobby lobby)
        {
            StartLobby();
            gameObject.SetActive(false);
            gamePanel.SetActive(true);
            opponentInputField.text = "";
            var game = gamePanel.GetComponent<TTTGameRest>();
            game.init(lobby);
        }

        public void JoinLobbyCallback(ServerMessage serverMessage)
        {
            if (serverMessage.IsError())
            {
                popup.SetMessage(serverMessage.message);
                return;
            }

            currentLobby = JsonConvert.DeserializeObject<ServerLobby>(serverMessage.message);
            if (currentLobby.players.Count == 2) GoToGamePanel(currentLobby);
        }

        public void HandleLobbyData(ServerMessage serverMessage)
        {
            if (serverMessage.IsError())
            {
                popup.SetMessage(serverMessage.message);
                return;
            }

            Debug.Log(serverMessage);
            currentLobby = JsonConvert.DeserializeObject<ServerLobby>(serverMessage.message);
        }

        #region ServerCalls

        //This methods gets called repetitively from a Timer
        public async void UpdateLobby()
        {
            if (lobbyID.IsNullOrEmpty())
                return;

            //do request
            var dataToSend = new Dictionary<string, object>
            {
                { "id", lobbyID }
            };

            await ServerCaller.Instance.GenericSendAsync("rest/get_lobby_by_id/", dataToSend, HandleLobbyData);

            //next panel/ start game
            if (currentLobby != null)
                if (currentLobby.players.Count == 2)
                    GoToGamePanel(currentLobby);
        }


        //set which lobby has started the match/game
        public async void StartLobby()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", lobbyID },
                { "startGame", "True" }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/set_lobby_by_id/", dataToSend);
        }


        public async void CreateLobby()
        {
            lobbyID = opponentInputField.text;
            var dataToSend = new Dictionary<string, object>
            {
                { "id", lobbyID },
                { "host", TemplateSettings.username }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/create_lobby/", dataToSend, popup.DefaultCallback);
            informationLabel.text = "Waiting for other player";
        }

        public async void JoinLobby()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "lobbyId", opponentInputField.text },
                { "id", TemplateSettings.username }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/join_lobby/", dataToSend, JoinLobbyCallback);
        }

        #endregion
    }
}