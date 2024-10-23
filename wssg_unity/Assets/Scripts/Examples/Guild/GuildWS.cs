using System.Collections.Generic;
using Core.Websocket;
using MISC;
using TMPro;
using UnityEngine;

namespace Examples.Guild
{
    public class GuildWS : CommunicationWS
    {
        [SerializeField] private Popup _popup;

        [SerializeField] private TMP_InputField _inputField;

        private string placeholderForURL = "placeholder";

        // Start is called before the first frame update
        private void Start()
        {
            url = "GuildWS/placeholder";
            ConnectToUrl(GenerateURLfromPath(url));

            var dataToSend = new Dictionary<string, object>
            {
                { "test", "hello world" }
            };
            SendMessageAsync(GenerateServerMessage(dataToSend, "debug"));
        }

        public void JoinGuild()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "guildname", _inputField.text }
            };
            SendMessageAsync(GenerateServerMessage(dataToSend, "join"));
        }

        public void LeaveGuild()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "guildname", _inputField.text }
            };
            SendMessageAsync(GenerateServerMessage(dataToSend, "leave"));
        }

        public void DebugGuild()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "test", "hello world" }
            };
            SendMessageAsync(GenerateServerMessage(dataToSend, "debug"));
        }
    }
}