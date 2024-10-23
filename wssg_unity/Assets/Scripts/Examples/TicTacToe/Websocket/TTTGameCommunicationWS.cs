using System.Collections.Generic;
using System.Linq;
using Core.Websocket;
using MISC;
using Newtonsoft.Json;
using ServerClasses;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using WebSocketSharp;

namespace Examples.TicTacToe.Websocket
{
    /*
     * The websocket variant for TTT Game
     */
    public class TTTGameCommunicationWS : CommunicationWS
    {
        public TextMeshProUGUI lobbyInformationText;
        public Popup popup;
        public bool showMessage;

        [SerializeField] private GameObject lobbyPanel;
        private ServerTTTGame currentGame = new();
        public Button[,] gameField = new Button[3, 3];
        public TextMeshProUGUI[,] gameFieldText = new TextMeshProUGUI[3, 3];
        private ServerMessage lastMessage = new();

        private ServerLobby lobby = new();


        //new variables needed to delay the UI updating
        //The UI cannot be updated outside of the main thread
        private bool updateField;

        private void Update()
        {
            /*
             * UI, GameObject updates cannot be on another thread...
             */
            if (showMessage)
            {
                showMessage = false;
                popup.SetMessage(lastMessage);
            }

            if (!updateField)
                return;

            //TTTGameRest.cs -> UpdateFieldBasedOnServerData

            for (int i = 0, x = 0; i < 3; i++)
            for (var j = 0; j < 3; j++, x++)
            {
                if (currentGame.action == null)
                    return;
                var fieldFromServer = JsonConvert.DeserializeObject<List<string>>(currentGame.action);
                gameFieldText[i, j].text = fieldFromServer[x];
                if (!fieldFromServer[x].IsNullOrEmpty())
                    gameField[i, j].interactable = false;
            }

            var result = checkCondition();
            switch (result)
            {
                case "None":
                    return;
                case "Draw":
                    EndGame("DRAW");
                    break;
                default:
                    EndGame(result.Equals("X") ? currentGame.host : currentGame.opponent);
                    break;
            }

            updateField = false;
        }

        public void ResetGame()
        {
            currentGame = new ServerTTTGame();
            lobby = new ServerLobby();

            lastMessage = new ServerMessage();

            for (var i = 0; i < 3; i++)
            for (var j = 0; j < 3; j++)
            {
                if (gameFieldText[i, j] == null)
                    gameFieldText[i, j] = transform.GetChild(1).GetChild(i * 3 + j)
                        .GetComponentInChildren<TextMeshProUGUI>();

                gameFieldText[i, j].text = "";
            }

            SetFieldTo(true);
        }

        public bool IsHost()
        {
            return currentGame.host.Equals(TemplateSettings.username);
        }

        public void init(ServerLobby serverLobby)
        {
            ResetGame();
            lobby = serverLobby;

            //sets host and opponent
            currentGame.host = serverLobby.players[0];
            currentGame.opponent = serverLobby.players[1];

            //NEW url for ws
            url = "TTTGame/" + lobby.lobbyID;

            //get the references etc. could also be done in the inspector if one doesn't want to use GetChild/GetComponent 
            for (var i = 0; i < 3; i++)
            for (var j = 0; j < 3; j++)
            {
                // Assuming gameField and gameFieldText arrays are initialized with GameObjects
                gameField[i, j] = transform.GetChild(1).GetChild(i * 3 + j).GetComponent<Button>();
                gameFieldText[i, j] =
                    transform.GetChild(1).GetChild(i * 3 + j).GetComponentInChildren<TextMeshProUGUI>();

                //the indices needs to be copied, otherwise wrong calls!
                var copyX = i;
                var copyY = j;

                //set event/onClick
                gameField[i, j].onClick.AddListener(() => SetButtons(copyX, copyY));
            }

            lobbyInformationText.text = currentGame.host;

            //since the syncing between clients is being done with a broadcast. The client only needs to connect to the server
            ConnectToUrl(GenerateURLfromPath(url));

            if (IsHost())
                CreateServerGame();
        }

        /*
         * what should happen on every button click?
         * sets the label, and sends the action to the server
         */
        public void SetButtons(int x, int y)
        {
            var currentPlayer = currentGame.current_index == 0 ? currentGame.host : currentGame.opponent;
            if (!currentPlayer.Equals(TemplateSettings.username))
                return;

            gameFieldText[x, y].text = currentGame.current_index == 0 ? "X" : "O";
            gameField[x, y].interactable = false;
            currentGame.current_index++;
            currentGame.current_index %= 2;
            lobbyInformationText.text = currentPlayer;


            //send action to server
            UpdateServerAction();

            //check winning condition
            var result = checkCondition();
            switch (result)
            {
                case "None":
                    return;
                case "Draw":
                    EndGame("DRAW");
                    break;
                default:
                    EndGame(result.Equals("X") ? currentGame.host : currentGame.opponent);
                    break;
            }
        }


        //set UI, disables Timer,and end game on server
        public void EndGame(string resultOfGame)
        {
            if (!IsHost())
                return;
            popup.SetMessage(resultOfGame);
            lobbyInformationText.text =
                (currentGame.current_index + 1) % 2 == 0 ? currentGame.host : currentGame.opponent;
            SetFieldTo();

            EndGameServer(resultOfGame);
        }

        public void SetFieldTo(bool inputB = false)
        {
            for (var i = 0; i < 3; i++)
            for (var j = 0; j < 3; j++)
            {
                if (gameField[i, j] == null)
                    gameField[i, j] = transform.GetChild(1).GetChild(i * 3 + j).GetComponent<Button>();
                gameField[i, j].interactable = inputB;
            }
        }

        //winning condition goes brrr
        public string checkCondition()
        {
            // Check rows
            for (var i = 0; i < 3; i++)
                if (gameFieldText[i, 0].text != "" && gameFieldText[i, 0].text == gameFieldText[i, 1].text &&
                    gameFieldText[i, 0].text == gameFieldText[i, 2].text)
                    return gameFieldText[i, 0].text;

            // Check columns
            for (var j = 0; j < 3; j++)
                if (gameFieldText[0, j].text != "" && gameFieldText[0, j].text == gameFieldText[1, j].text &&
                    gameFieldText[0, j].text == gameFieldText[2, j].text)
                    return gameFieldText[0, j].text;

            // Check diagonals
            if (gameFieldText[0, 0].text != "" && gameFieldText[0, 0].text == gameFieldText[1, 1].text &&
                gameFieldText[0, 0].text == gameFieldText[2, 2].text)
                return gameFieldText[0, 0].text;

            if (gameFieldText[0, 2].text != "" && gameFieldText[0, 2].text == gameFieldText[1, 1].text &&
                gameFieldText[0, 2].text == gameFieldText[2, 0].text)
                return gameFieldText[0, 2].text;

            // Check for draw
            var draw = true;
            for (var i = 0; i < 3; i++)
            for (var j = 0; j < 3; j++)
                if (gameFieldText[i, j].text == "")
                {
                    draw = false;
                    break;
                }

            if (draw)
                return "Draw";

            // If no winner and not a draw, return "None"
            return "None";
        }

        //parse the field to a json string
        public string GameToJson()
        {
            var resultField = new List<string>();
            for (int i = 0, x = 0; i < 3; i++)
            for (var j = 0; j < 3; j++, x++)
                // Assuming gameField and gameFieldText arrays are initialized with GameObjects
                resultField.Add(gameFieldText[i, j].text);

            return JsonConvert.SerializeObject(resultField);
        }

        //this method is the "WS variant" for the whole timer update thing
        public override void WsOnOnMessage(object sender, MessageEventArgs e)
        {
            //handle responses
            var serverMessage = JsonConvert.DeserializeObject<ServerMessage>(e.Data);

            if (serverMessage.message.Contains("terminated"))
            {
                var surrenderBtn = GetComponentsInChildren<Button>().Last();
                Debug.Log(surrenderBtn.name);
                surrenderBtn.onClick.Invoke();
            }

            if (serverMessage.IsShowMessage())
                showMessage = true; //delay update of UI

            if (serverMessage.IsData())
                //one if needed, just to prepare for the future 
                switch (serverMessage.extraMessage)
                {
                    case "gameData":
                        currentGame = JsonConvert.DeserializeObject<ServerTTTGame>(serverMessage.message);
                        updateField = true; //delay update of UI
                        break;
                }

            lastMessage = serverMessage;
        }


        //The SAME SERVERCALLS as TTTGameRest.cs

        #region ServerCalls

        public void CreateServerGame()
        {
            Debug.Log("Create Game");
            var dataToSend = new Dictionary<string, object>
            {
                { "lobbyId", lobby.lobbyID },
                { "host", currentGame.host },
                { "opponent", currentGame.opponent }
            };
            //no specific url is needed since the mapping from "url" in this case the identifier to python method is done in the respective python file
            SendMessageAsync(GenerateServerMessage(dataToSend, "CREATE GAME"));
        }


        public void UpdateServerAction()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "lobbyId", lobby.lobbyID },
                { "host", currentGame.host },
                { "opponent", currentGame.opponent },

                { "field", GameToJson() },
                { "current_index", currentGame.current_index }
            };

            //no specific url is needed since the mapping from "url" in this case the identifier to python method is done in the respective python file
            SendMessageAsync(GenerateServerMessage(dataToSend, "UPDATE GAME"));
        }

        //Surrender Game
        public void Surrender()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "lobbyId", lobby.lobbyID }
            };

            //no specific url is needed since the mapping from "url" in this case the identifier to python method is done in the respective python file
            SendMessageAsync(GenerateServerMessage(dataToSend, "SURRENDER GAME"));
            lobbyPanel.SetActive(true);
            gameObject.SetActive(false);
        }

        public void EndGameServer(string resultOfGame)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "host", currentGame.host },
                { "opponent", currentGame.opponent },
                { "playerWon", resultOfGame },
                { "lobbyId", lobby.lobbyID }
            };

            //no specific url is needed since the mapping from "url" in this case the identifier to python method is done in the respective python file
            SendMessageAsync(GenerateServerMessage(dataToSend, "END GAME"));
        }

        #endregion
    }
}