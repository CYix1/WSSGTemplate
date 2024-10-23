using System.Collections.Generic;
using Core.Rest;
using MISC;
using Newtonsoft.Json;
using ServerClasses;
using TMPro;
using UnityEngine;

/*
 * Script which handles the Leaderboard stuff in Scenes/Examples/REST/Leaderboard
 */
namespace Examples.Leaderboard.Rest
{
    public class LeaderBoardREST : MonoBehaviour
    {
        [Header("References")] public TextMeshProUGUI leaderboardNameLabel;


        public GameObject listEntryPrefab;
        public GameObject otherPanel;
        public GameObject contentParent;
        public Popup popup;
        private int currentScoreOfPlayer;

        private ServerLeaderboard leaderboard;

        public void init(ServerLeaderboard leaderboard)
        {
            this.leaderboard = leaderboard;
            leaderboardNameLabel.text = "Leaderboard:\n" + leaderboard.category;
            GenerateLeaderboard();

            //set the currentScoreOfPlayer 

            SetScoreFromData();
        }

        //use the leaderboard data to set the currentScoreOfPlayer. 
        //this way one does not start from 0 every time!
        private void SetScoreFromData()
        {
            for (var i = 0; i < leaderboard.entries.Count; i++)
                if (leaderboard.entries[i].player.Equals(TemplateSettings.username))
                    currentScoreOfPlayer = leaderboard.entries[i].score;
        }

        //generates the UI
        public void GenerateLeaderboard()
        {
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

        //what should happen with the new data from the server?
        public void UpdateLeaderboardFromServerCallback(ServerMessage serverMessage)
        {
            if (serverMessage.IsData())
            {
                leaderboard = JsonConvert.DeserializeObject<ServerLeaderboard>(serverMessage.message);
                SetScoreFromData();

                GenerateLeaderboard();
            }
            else
            {
                popup.SetMessage(serverMessage);
            }
        }


        //if set in the inspector, unnecessary method
        public void GoBack()
        {
            gameObject.SetActive(false);
            otherPanel.SetActive(true);
        }

        #region ServerCalls

        //servercall to increase the score
        public async void IncrementScore()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "category", leaderboard.category },
                { "score", currentScoreOfPlayer + 1 }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/update_score_of_player/", dataToSend,
                popup.DefaultCallback);
        }

        //request new information about the leaderboard
        //This methods gets called repetitively from a Timer
        public async void UpdateLeaderboardFromServer()
        {
            if (leaderboard == null)
                return;
            var dataToSend = new Dictionary<string, object>
            {
                { "category", leaderboard.category },
                { "order", "desc" }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/get_complete_leaderboard_by_category/", dataToSend,
                UpdateLeaderboardFromServerCallback);
        }

        #endregion
    }
}