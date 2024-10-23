using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using Newtonsoft.Json;
using ServerClasses;
using UnityEngine;
using UnityEngine.Networking;
using Utility;
using WebSocketSharp;

namespace Core.Rest
{
    /*
     * This class is a singleton which mostly does the rest communication between unity and django
     * The most important methods are GenericSend and GenericRequest.
     * Both methods are available in as Coroutines or as async version
     *
     * https://docs.unity3d.com/Manual/Coroutines.html
     * https://gamedevbeginner.com/async-in-unity/
     */
    public class ServerCaller : SingletonPersistant<ServerCaller>
    {
        //two Callbacks for either a normal string response or the preconfigured ServerMessage
        public delegate void ServerRequestCallBack(ServerMessage response);

        public delegate void ServerRequestDefaultCallback(string response);

        public void GenericSendCall(string url, Dictionary<string, object> values,
            ServerRequestCallBack callback = null)
        {
            StartCoroutine(GenericSend(url, values, callback));
        }

        public void GenericSendCall(string url, WWWForm form, ServerRequestCallBack callback = null)
        {
            StartCoroutine(GenericSend(url, form, callback));
        }

        public void GenericRequestCall(string url, ServerRequestCallBack callback = null)
        {
            StartCoroutine(GenericRequest(url, callback));
        }

        public void DelegateTest()
        {
            Debug.Log("example callback");
        }

        public IEnumerator GenericSend(string url, Dictionary<string, object> values,
            ServerRequestCallBack callback = null)
        {
            //little safety check
            if (!url.StartsWith(TemplateSettings.url))
                url = TemplateSettings.url + url;
            using (var www = UnityWebRequest.Post(url, JsonConvert.SerializeObject(values), "application/json"))
            {
                yield return www.SendWebRequest();
                if (www.downloadHandler.text.IsNullOrEmpty())
                    throw new Exception("Server did not respond. Is the server up? or does it receive the request?");

                callback?.Invoke(JsonConvert.DeserializeObject<ServerMessage>(www.downloadHandler.text));
            }
        }

        public IEnumerator GenericSend(string url, WWWForm form, ServerRequestCallBack callback = null)
        {
            //little safety check
            if (!url.StartsWith(TemplateSettings.url))
                url = TemplateSettings.url + url;

            using (var www = UnityWebRequest.Post(url, form))
            {
                yield return www.SendWebRequest();
                if (www.downloadHandler.text.IsNullOrEmpty())
                    throw new Exception("Server did not respond. Is the server up? or does it receive the request?");
                Debug.Log(www.downloadHandler.text);
                callback?.Invoke(JsonConvert.DeserializeObject<ServerMessage>(www.downloadHandler.text));
            }
        }

        public IEnumerator GenericRequest(string url, ServerRequestCallBack callback = null)
        {
            //little safety check
            if (!url.StartsWith(TemplateSettings.url))
                url = TemplateSettings.url + url;
            using (var www = UnityWebRequest.PostWwwForm(url, ""))
            {
                yield return www.SendWebRequest();
                if (www.downloadHandler.text.IsNullOrEmpty())
                    throw new Exception("Server did not respond. Is the server up? or does it receive the request?");
                Debug.Log(www.downloadHandler.text);
                callback?.Invoke(JsonConvert.DeserializeObject<ServerMessage>(www.downloadHandler.text));
            }
        }


        public async Task GenericSendAsync(string url, Dictionary<string, object> values,
            ServerRequestCallBack callback = null)
        {
            //little safety check
            if (!url.StartsWith(TemplateSettings.url))
                url = TemplateSettings.url + url;
            using (var www = UnityWebRequest.Post(url, JsonConvert.SerializeObject(values), "application/json"))
            {
                await www.SendWebRequest();
                while (!www.isDone)
                    await Task.Yield();
                if (www.downloadHandler.text.IsNullOrEmpty())
                    throw new Exception("Server did not respond. Is the server up? or does it receive the request?");

                Debug.Log(www.downloadHandler.text);
                callback?.Invoke(JsonConvert.DeserializeObject<ServerMessage>(www.downloadHandler.text));
            }
        }

        public async Task GenericSendAsync(string url, WWWForm form, ServerRequestCallBack callback = null)
        {
            //little safety check
            if (!url.StartsWith(TemplateSettings.url))
                url = TemplateSettings.url + url;
            using (var www = UnityWebRequest.Post(url, form))
            {
                await www.SendWebRequest();
                while (!www.isDone)
                    await Task.Yield();
                if (www.downloadHandler.text.IsNullOrEmpty())
                    throw new Exception("Server did not respond. Is the server up? or does it receive the request?");

                callback?.Invoke(JsonConvert.DeserializeObject<ServerMessage>(www.downloadHandler.text));
            }
        }

        public async Task GenericRequestAsync(string url, ServerRequestCallBack callback = null)
        {
            //little safety check
            if (!url.StartsWith(TemplateSettings.url))
                url = TemplateSettings.url + url;
            using (var www = UnityWebRequest.PostWwwForm(url, ""))
            {
                await www.SendWebRequest();
                while (!www.isDone)
                    await Task.Yield();
                if (www.downloadHandler.text.IsNullOrEmpty())
                    throw new Exception("Server did not respond. Is the server up? or does it receive the request?");

                callback?.Invoke(JsonConvert.DeserializeObject<ServerMessage>(www.downloadHandler.text));
            }
        }

        public static bool isHost(string user)
        {
            return user.Equals(TemplateSettings.username);
        }
    }
}