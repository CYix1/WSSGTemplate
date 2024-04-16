using ServerClasses;
using TMPro;
using UnityEngine;

/*
 * The UI "Wrapper" for BasicRestAuthentication.cs
 */
namespace BasicRest
{
    public class AuthUI : MonoBehaviour
    {
        [SerializeField] private TMP_InputField userInputField;

        [SerializeField] private TMP_InputField passwordInputField;

        public Authentication authenticator;

        public GameObject authPanel;
        public GameObject otherPanel;
        public Popup popup;

        private void OnEnable()
        {
            SetAuthenticatorVariables();
        }

        public void SetAuthenticatorVariables()
        {
            TemplateSettings.username = userInputField.text;

            authenticator.password = passwordInputField.text;
        }

        public void SigninSuccessCallback(ServerMessage serverMessage)
        {
            if (serverMessage.IsShowMessage())
                popup.SetMessage(serverMessage.message);
            if (serverMessage.identifier.Equals("ERROR"))
                return;
            authPanel.SetActive(false);
            otherPanel.SetActive(true);
        }

        public void SigninBtnCall()
        {
            SetAuthenticatorVariables();

            StartCoroutine(authenticator.signinWWW(SigninSuccessCallback));
        }

        public void SignupBtnCall()
        {
            SetAuthenticatorVariables();

            StartCoroutine(authenticator.signup(SigninSuccessCallback));
        }

        public void SignoutBtnCall()
        {
            SetAuthenticatorVariables();
            StartCoroutine(authenticator.signout());
        }
    }
}