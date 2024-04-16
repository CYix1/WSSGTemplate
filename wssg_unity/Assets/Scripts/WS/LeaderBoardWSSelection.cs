using TMPro;
using UnityEngine;

namespace WS
{
    public class LeaderBoardWSSelection : MonoBehaviour
    {
        public TMP_InputField categoryInput;
        public Popup popup;
        public GameObject leaderBoardPanel;

        //init
        public void OpenLeaderboard()
        {
            //switch panel
            leaderBoardPanel.SetActive(true);
            gameObject.SetActive(false);

            //initialise the next script
            var script = leaderBoardPanel.GetComponent<LeaderBoardCommunicationWS>();
            script.init(categoryInput.text);
        }
    }
}