using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;
using ServerClasses;
using UnityEngine;
using WebSocketSharp;

/*
 * A client for a websocket
 */
namespace WS
{
    public class CommunicationWS : MonoBehaviour
    {
        public string url = "basic/";
        public bool directConnect;
        public bool finishSetup;
        public WebSocket ws;


        public void OnEnable()
        {
            //fix url if needed
            if (!directConnect) return;
            ResetWS(url);

            if (isActiveAndEnabled)
                ConnectToUrl(GenerateURLfromPath(url));
            else
                // If the object is not active and enabled, use a coroutine to wait for it
                StartCoroutine(WaitAndConnect());
        }

        public void OnDisable()
        {
            ws.Close();
        }

        private IEnumerator WaitAndConnect()
        {
            // Wait until the object becomes active and enabled
            yield return new WaitUntil(() => isActiveAndEnabled);


            // Connect to the URL on the main thread
            ConnectToUrl(GenerateURLfromPath(url));
        }

        public void ConnectToUrl(string urlInput)
        {
            if (ws == null)
                ResetWS(urlInput);

            // Check if the object is active and enabled before proceeding
            ws.OnOpen += WsOnOnOpen;
            ws.OnClose += WsOnOnClose;
            ws.OnMessage += WsOnOnMessage;
            ws.OnError += WsOnOnError;

            // Connect asynchronously on the main thread
            ws.ConnectAsync();
            finishSetup = true;
        }


        public string GenerateURLfromPath(string urlInput)
        {
            var builder = new StringBuilder();
            builder.Append("ws://");
            builder.Append(TemplateSettings.url.Replace("http://", ""));
            builder.Append("ws/");
            builder.Append(urlInput);
            if (!urlInput.EndsWith("/"))
                builder.Append("/");
            Debug.Log($"<color=#FFF>{builder}</color>");
            return builder.ToString();
        }

        public void ResetWS(string urlInput)
        {
            if (!urlInput.Contains("ws://"))
            {
                
                urlInput = GenerateURLfromPath(urlInput);
            }


            ws = new WebSocket(urlInput);
        }

        public new void SendMessage(string message)
        {
            ws.Send(message);
        }


        public void SendMessageAsync(string message)
        {
            ws.SendAsync(message, DebugDelegate);
        }

        public void SendMessageAsync(ServerMessage serverMessage)
        {
            if (ws != null && ws.ReadyState == WebSocketState.Open)
            {
                ws.SendAsync(serverMessage.ToString(), DebugDelegate);
            }
            else
            {
                // WebSocket is not open, wait for it to be open
                StartCoroutine(WaitForWebSocket(serverMessage.ToString(), DebugDelegate));
            }
        }

        public void SendMessageAsync(ServerMessage serverMessage, Action<bool> completed)
        {
            // Check if WebSocket is in Open state
            if (ws != null && ws.ReadyState == WebSocketState.Open)
                ws.SendAsync(serverMessage.ToString(), completed);
            else
                // WebSocket is not open, wait for it to be open
                StartCoroutine(WaitForWebSocket(serverMessage.ToString(), completed));
        }

        // Coroutine to wait for WebSocket to be ready and then send the message
        private IEnumerator WaitForWebSocket(string message, Action<bool> completed)
        {
            // Wait until WebSocket state becomes Open
            while (ws == null || ws.ReadyState != WebSocketState.Open)
            {
                
                yield return null; // Wait for one frame
            }
            // Now that WebSocket is open, send the message
            ws.SendAsync(message, completed);
        }

        public void SendMessageAsync(string message, string identifier, Action<bool> completed, string username = null)
        {
            if (username == null)
                username = TemplateSettings.username;

            SendMessageAsync(new ServerMessage(username, message, identifier), completed);
        }

        //what should happen when the response is successful or not
        public void DebugDelegate(bool b)
        {
            //Debug.Log("delegate | " + b);
        }

        //predefined structure for requests to the server
        public ServerMessage GenerateServerMessage(Dictionary<string, object> values, string identifier,
            string extraMessage = null)
        {
            //sanity check if the connection is open
            if (ws == null || ws.ReadyState == WebSocketState.Closed)
                ConnectToUrl(GenerateURLfromPath(url));


            var serverMessage = new ServerMessage();
            serverMessage.extraMessage = extraMessage ?? TemplateSettings.username;
            serverMessage.identifier = identifier;
            serverMessage.message = JsonConvert.SerializeObject(values);

            return serverMessage;
        }


        #region Default methods

        public virtual void WsOnOnOpen(object sender, EventArgs e)
        {
            Debug.Log("Websocket Connected! " + e);
        }

        public virtual void WsOnOnClose(object sender, CloseEventArgs e)
        {
            Debug.Log($"Websocket Closed! \nCode:{e.Code}\nReason{e.Reason}\n");

            Debug.Log("possible ERROR sources:\n" +
                      "is the server open?\n" +
                      "is the path correct?\n" +
                      "does the websocket implementation exists?"
            );
        }

        public virtual void WsOnOnMessage(object sender, MessageEventArgs e)
        {
            Debug.Log($"Server message({sender}): " + e.Data);
        }

        public virtual void WsOnOnError(object sender, ErrorEventArgs e)
        {
            Debug.LogError($"Server Error {sender}\n{e.Message}\n{e.Exception}");
        }

        #endregion
    }
}