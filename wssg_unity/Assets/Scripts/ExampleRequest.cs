using System.Collections.Generic;
using ServerClasses;
using UnityEngine;

public class ExampleRequest : MonoBehaviour
{
    public Popup popup;

    public async void Request()
    {
        var dataToSend = new Dictionary<string, object>
        {
            { "username", "USERNAME" },
            { "password", "PASSWORD" }
        };
        await ServerCaller.Instance.GenericSendAsync("rest/signin/", dataToSend, Callback);
    }

    public void Callback(ServerMessage serverMessage)
    {
        Debug.Log(serverMessage);
        popup.DefaultCallback(serverMessage);
    }
}