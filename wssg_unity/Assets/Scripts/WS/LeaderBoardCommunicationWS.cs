using System.Collections.Generic;
using Newtonsoft.Json;
using ServerClasses;
using TMPro;
using UnityEngine;
using WebSocketSharp;

namespace WS
{
    public class LeaderBoardCommunicationWS : CommunicationWS
    {
        [Header("References")] public TextMeshProUGUI leaderboardNameLabel;


        public GameObject listEntryPrefab;
        public GameObject otherPanel;
        public GameObject contentParent;
        public Popup popup;
        private int currentScoreOfPlayer = -1;
        private ServerMessage lastMessage;
        private ServerLeaderboard leaderboard;
        private bool showMessage;
        private bool updateBoard;

        private void Update()
        {
            if (showMessage)
            {
                showMessage = false;
                popup.SetMessage(lastMessage);
            }

            if (!updateBoard)
                return;

            Debug.Log("update BOard");
            SetScoreFromData();

            GenerateLeaderboard();
            updateBoard = false;
        }

        public void init(string leaderBoardName)
        {
            url = "WSLeaderboard/" + leaderBoardName;
            leaderboardNameLabel.text = "Leaderboard:\n" + leaderBoardName;
            GenerateLeaderboard();

            //set the currentScoreOfPlayer 

            SetScoreFromData();
            ConnectToUrl(GenerateURLfromPath(url));
            IncrementScore();
        }

        //use the leaderboard data to set the currentScoreOfPlayer. 
        //this way one does not start from 0 every time!
        private void SetScoreFromData()
        {
            if (leaderboard == null)
                return;
            for (var i = 0; i < leaderboard.entries.Count; i++)
                if (leaderboard.entries[i].player.Equals(TemplateSettings.username))
                    currentScoreOfPlayer = leaderboard.entries[i].score;
        }

        //generates the UI
        public void GenerateLeaderboard()
        {
            if (leaderboard == null)
                return;
            //reset the UI by destroying all items
            foreach (Transform VARIABLE in contentParent.transform) Destroy(VARIABLE.gameObject);
            for (var i = 0; i < leaderboard.entries.Count; i++)
            {
                var listEntry = Instantiate(listEntryPrefab, contentParent.transform);
                listEntry.transform.GetChild(0).GetComponent<TextMeshProUGUI>().text = leaderboard.entries[i].player;
                listEntry.transform.GetChild(1).GetComponent<TextMeshProUGUI>().text =
                    "" + leaderboard.entries[i].score;
            }
        }


        //if set in the inspector, unnecessary method
        public void GoBack()
        {
            gameObject.SetActive(false);
            otherPanel.SetActive(true);
        }

        public override void WsOnOnMessage(object sender, MessageEventArgs e)
        {
            Debug.Log(e.Data);
            //handle responses
            var serverMessage = JsonConvert.DeserializeObject<ServerMessage>(e.Data);

            if (serverMessage.IsShowMessage())
                showMessage = true; //delay update of UI

            if (serverMessage.IsData())
                //one if needed, just to prepare for the future 
                switch (serverMessage.extraMessage)
                {
                    case "leader_board_data":
                        leaderboard = JsonConvert.DeserializeObject<ServerLeaderboard>(serverMessage.message);
                        updateBoard = true; //delay update of UI
                        break;
                }

            Debug.Log(serverMessage);
            lastMessage = serverMessage;
        }

        #region ServerCalls

        //servercall to increase the score
        public void IncrementScore()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "category", url.Split("/")[1] },
                { "score", currentScoreOfPlayer + 1 }
            };
            SendMessageAsync(GenerateServerMessage(dataToSend, "UPDATE ENTRY"));
        }

        #endregion
    }
}