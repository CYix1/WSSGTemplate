using MISC;
using TMPro;
using UnityEngine;

namespace Examples.Chat
{
    public class ChatSelectionWS : MonoBehaviour
    {
        public TMP_InputField categoryInput;
        public Popup popup;
        public GameObject chatPanel;

        //init
        public void OpenChat()
        {
            //switch panel
            chatPanel.SetActive(true);
            gameObject.SetActive(false);

            //initialise the next script
            var script = chatPanel.GetComponent<ChatCommunicationWS>();
            script.init(categoryInput.text);
        }
    }
}