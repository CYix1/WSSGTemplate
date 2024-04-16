using System.Collections.Generic;
using Newtonsoft.Json;
using ServerClasses;
using TMPro;
using UnityEngine;

/*
 * Script which handles the Leaderboard stuff in Scenes/Examples/REST/Leaderboard
 * The first screen e.g the selection screen
 */
namespace BasicRest
{
    public class LeaderBoardSelection : MonoBehaviour
    {
        public TMP_InputField categoryInput;
        public Popup popup;
        public GameObject leaderBoardPanel;

        //servercall
        public async void OpenLeaderboard()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "category", categoryInput.text }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/get_complete_leaderboard_by_category/", dataToSend,
                OpenLeaderboardCallback);
        }

        //callback
        public void OpenLeaderboardCallback(ServerMessage serverMessage)
        {
            if (!serverMessage.IsData())
                return;

            //switch panel
            leaderBoardPanel.SetActive(true);
            gameObject.SetActive(false);

            //initialise the next script
            var script = leaderBoardPanel.GetComponent<LeaderBoardREST>();
            var leaderboard = JsonConvert.DeserializeObject<ServerLeaderboard>(serverMessage.message);
            script.init(leaderboard);

            //show message
            popup.SetMessage(serverMessage);
        }
    }
}