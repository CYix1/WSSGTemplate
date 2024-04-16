using System.Collections.Generic;
using System.Linq;
using Newtonsoft.Json;
using ServerClasses;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using WebSocketSharp;

namespace BasicRest
{
    public class TTTGameRest : MonoBehaviour
    {
        public TextMeshProUGUI lobbyInformationText;
        public Popup popup;
        private ServerTTTGame currentGame = new();
        public Button[,] gameField = new Button[3, 3];
        public TextMeshProUGUI[,] gameFieldText = new TextMeshProUGUI[3, 3];

        private ServerLobby lobby = new();
        [SerializeField] private GameObject lobbyPanel;

        public bool isHost()
        {
            return currentGame.host.Equals(TemplateSettings.username);
        }

        public void ResetGame()
        {
            currentGame =  new();
            lobby =  new();

            
            for (var i = 0; i < 3; i++)
            for (var j = 0; j < 3; j++)
            {
                if (gameFieldText[i, j] == null)
                    gameFieldText[i, j] = transform.GetChild(1).GetChild(i * 3 + j).GetComponentInChildren<TextMeshProUGUI>();

                gameFieldText[i, j].text = "";
            }
            SetFieldTo(true);
        }

        public void init(ServerLobby serverLobby)
        {
            ResetGame();
            lobby = serverLobby;

            //sets host and opponent
            currentGame.host = serverLobby.players[0];
            currentGame.opponent = serverLobby.players[1];

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
          
            if (isHost()) //only one person needs to create the game on the server!
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
            gameField[x, y].interactable = false; //disables button to prevent further interaction
            currentGame.current_index++;
            currentGame.current_index %= 2; //2P game
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
            popup.SetMessage(resultOfGame);
            lobbyInformationText.text =
                (currentGame.current_index + 1) % 2 == 0 ? currentGame.host : currentGame.opponent;
            SetFieldTo();
            var timer = GetComponent<Timer>();
            timer.stopped = true;

            EndGameServer(resultOfGame);
        }


      
        public void SetFieldTo(bool inputB=false)
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


        public void UpdateFieldBasedOnServerData(ServerMessage serverMessage)
        {
            

            if (serverMessage.IsShowMessage()) popup.SetMessage(serverMessage.message);

            if (serverMessage.IsData()) //data from the server is being received
            {
                currentGame = JsonConvert.DeserializeObject<ServerTTTGame>(serverMessage.message);

                //set the field from the server   
                for (int i = 0, x = 0; i < 3; i++)
                for (var j = 0; j < 3; j++, x++)
                {
                    var fieldFromServer = JsonConvert.DeserializeObject<List<string>>(currentGame.action);
                    gameFieldText[i, j].text = fieldFromServer[x];

                    //button has text => disable it
                    if (!fieldFromServer[x].IsNullOrEmpty())
                        gameField[i, j].interactable = false;
                }

                //double check winning condition
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
        }

        public void HandleSurrenderCallback(ServerMessage response)
        {
            popup.SetMessage(response.message);
            lobbyPanel.SetActive(true);
            gameObject.SetActive(false);
            
        }

        #region ServerCalls

        public async void CreateServerGame()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "lobbyId", lobby.lobbyID },
                { "host", currentGame.host },
                { "opponent", currentGame.opponent }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/create_game/", dataToSend, popup.DefaultCallback);
        }


        public async void UpdateServerAction()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "lobbyId", lobby.lobbyID },
                { "host", currentGame.host },
                { "opponent", currentGame.opponent },

                { "field", GameToJson() },
                { "current_index", currentGame.current_index }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/update_game_action/", dataToSend, popup.DefaultCallback);
        }

        //Surrender Game
        public async void Surrender()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "lobbyId", lobby.lobbyID }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/surrender_game/", dataToSend, HandleSurrenderCallback);

        }
        
        public async void EndGameServer(string resultOfGame)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "host", currentGame.host },
                { "opponent", currentGame.opponent },
                { "playerWon", resultOfGame },
                { "lobbyId", lobby.lobbyID }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/end_game/", dataToSend, popup.DefaultCallback);
        }

        public async void UpdateFieldFromServer()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "host", currentGame.host },
                { "opponent", currentGame.opponent },
                { "lobbyId", lobby.lobbyID }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/get_game/", dataToSend, UpdateFieldBasedOnServerData);
        }

        #endregion
    }
}