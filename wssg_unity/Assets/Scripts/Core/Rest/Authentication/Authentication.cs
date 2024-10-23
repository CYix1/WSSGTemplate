using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using MISC;
using UnityEngine;

/*
 * Handles basic REST authentication in multiple variants.
 * password SHOULD NOT BE SET TODO
 */
namespace Core.Rest.Authentication
{
    public class Authentication : MonoBehaviour
    {
        public string password = "";
        public Popup popup; //TODO change to private and contructor?

        public IEnumerator signin(ServerCaller.ServerRequestCallBack callback = null)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "username", TemplateSettings.username },
                { "password", password }
            };
            yield return ServerCaller.Instance.GenericSend("rest/signin/", dataToSend,
                callback ?? popup.DefaultCallback);
        }

        public IEnumerator signinWWW(ServerCaller.ServerRequestCallBack callback = null)
        {
            var form = new WWWForm();
            form.AddField("username", TemplateSettings.username);
            form.AddField("password", password);

            yield return ServerCaller.Instance.GenericSend("rest/signin/", form, callback ?? popup.DefaultCallback);
        }


        public async Task signinAsync(ServerCaller.ServerRequestCallBack callback = null)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "username", TemplateSettings.username },
                { "password", password }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/signin/", dataToSend, callback ?? popup.DefaultCallback);
        }


        public IEnumerator signinForm(ServerCaller.ServerRequestCallBack callback = null)
        {
            var form = new WWWForm();
            form.AddField("username", TemplateSettings.username);
            form.AddField("password", password);
            yield return ServerCaller.Instance.GenericSend("rest/signin/", form, callback ?? popup.DefaultCallback);
        }

        public IEnumerator signup(ServerCaller.ServerRequestCallBack callback = null)
        {
            var form = new WWWForm();
            form.AddField("username", TemplateSettings.username);
            form.AddField("password1", password);
            form.AddField("password2", password);
            yield return ServerCaller.Instance.GenericSend("rest/signup/", form, callback ?? popup.DefaultCallback);
        }

        public IEnumerator signout(ServerCaller.ServerRequestCallBack callback = null)
        {
            TemplateSettings.username = "";

            yield return ServerCaller.Instance.GenericRequest("rest/signout/", callback ?? popup.DefaultCallback);
        }


        #region ContextMenues

        [ContextMenu("signin")]
        public void signinCTM()
        {
            StartCoroutine(signin());
        }

        [ContextMenu("signinAsync")]
        public async void signinAsyncCTM()
        {
            await signinAsync();
        }

        [ContextMenu("signup")]
        public void signupCTM()
        {
            StartCoroutine(signup());
        }

        [ContextMenu("signout")]
        public void signoutCTM()
        {
            StartCoroutine(signout());
        }

        #endregion
    }
}