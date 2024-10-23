using System.Collections.Generic;
using Core.Rest;
using MISC;
using TMPro;
using UnityEngine;

namespace Examples.Guild
{
    public class GuildRest : MonoBehaviour
    {
        [SerializeField] private Popup _popup;

        [SerializeField] private TMP_InputField _inputField;

        public async void JoinGuildServerCall()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "guildname", _inputField.text }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/join_guild/", dataToSend, _popup.DefaultCallback);
        }

        public async void LeaveGuildServerCall()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "guildname", _inputField.text }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/leave_guild/", dataToSend, _popup.DefaultCallback);
        }

        public async void DebugGuildServerCall()
        {
            await ServerCaller.Instance.GenericRequestAsync("rest/debug_guild/", _popup.DefaultCallback);
        }
    }
}