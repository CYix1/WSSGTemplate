using System;
using System.Collections.Generic;
using Core.Rest;
using Core.Websocket;
using MISC;
using Newtonsoft.Json;
using ServerClasses;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using WebSocketSharp;

namespace Examples.Chat
{
    public class ChatCommunicationWS : CommunicationWS
    {
        [Header("References")] public TextMeshProUGUI chatGroupNameLabel;

        public TMP_InputField messageInput;

        public GameObject chatMessagePrefab;
        public GameObject contentParent;
        public Popup popup;
        public ScrollRect scrollRect;
        private ServerChat chat;
        private string chatGroupName;
        private ServerChat.Message lastChatMessage;
        private ServerMessage lastMessage;
        private bool showMessage;
        private bool updateChat;

        public void init(string chatName)
        {
            chatGroupName = chatName;
            url = "ChatWS/" + chatName;

            GenerateUI();

            ConnectToUrl(GenerateURLfromPath(url));
            Debug.Log(ws.ReadyState);
            var dataToSend = new Dictionary<string, object>
            {
                { "name", chatName }
            };
            SendMessageAsync(GenerateServerMessage(dataToSend, "UPDATE ENTRY"));

            Debug.Log(ws.ReadyState);
        }

        // Function to scroll the ScrollRect down
        public void ScrollDown()
        {
            scrollRect.normalizedPosition = new Vector2(0, 0);
        }

        #region Server Calls

        public void SendChatMessage()
        {
            var message = new ServerChat.Message(TemplateSettings.username, DateTime.Now, messageInput.text);
            var dataToSend = new Dictionary<string, object>
            {
                { "message", message },
                { "name", chatGroupName }
            };
            SendMessageAsync(GenerateServerMessage(dataToSend, "UPDATE ENTRY"));
        }

        #endregion

        #region UI generation

        public void GenerateUI()
        {
            if (chat == null)
                return;
            for (var i = 0; i < chat.messages.Count; i++)
            {
                var message = chat.messages[i];

                if (lastChatMessage == null || message.time > lastChatMessage.time)
                {
                    var listEntry = Instantiate(chatMessagePrefab, contentParent.transform);
                    if (ServerCaller.isHost(message.username))
                        listEntry.transform.GetChild(0).GetComponent<TextMeshProUGUI>().text =
                            "<color=#222>" + message.username + "</color>";
                    else
                        listEntry.transform.GetChild(0).GetComponent<TextMeshProUGUI>().text = message.username;
                    listEntry.transform.GetChild(1).GetComponent<TextMeshProUGUI>().text =
                        "<color=#222>" + message.time + "</color>";
                    listEntry.transform.GetChild(2).GetComponent<TextMeshProUGUI>().text = message.message;
                }
            }
        }

        private void Update()
        {
            if (showMessage)
            {
                showMessage = false;
                popup.SetMessage(lastMessage);
            }

            if (!updateChat)
                return;

            Debug.Log("update chat");

            GenerateUI();

            ScrollDown();
            updateChat = false;
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
                    case "chat_data":
                        if (chat != null && chat.messages.Count > 0)
                            lastChatMessage = chat.messages[^1];

                        Debug.Log(serverMessage.message);
                        chat = JsonConvert.DeserializeObject<ServerChat>(serverMessage.message);
                        updateChat = true; //delay update of UI
                        break;
                }

            Debug.Log(serverMessage);
            lastMessage = serverMessage;
        }

        #endregion
    }
}