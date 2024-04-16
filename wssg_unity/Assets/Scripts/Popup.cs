using ServerClasses;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

/*
 * A basic script which should handle a Pop up message.
 * Especially for errors or other messages
 */
public class Popup : MonoBehaviour
{
    public delegate void BtnCallback();

    public TextMeshProUGUI messageTMP;
    public Button acceptBtn;
    public Button declineBtn;

    public void SetMessage(string message, bool enableBtns = false)
    {
        acceptBtn.gameObject.SetActive(enableBtns);
        declineBtn.gameObject.SetActive(enableBtns);
        gameObject.SetActive(true);
        messageTMP.text = message;
    }

    public void SetMessage(ServerMessage serverMessage, bool enableBtns = false)
    {
        if (serverMessage.IsShowMessage())
            SetMessage(serverMessage.message);

        acceptBtn.gameObject.SetActive(enableBtns);
        declineBtn.gameObject.SetActive(enableBtns);
        gameObject.SetActive(true);
    }


    //two methods if one wants to use some kind of accept/decline popup
    public void SetMessageWithBtns(string message, BtnCallback acceptCallback, BtnCallback declineCallback)
    {
        SetMessage(message, true);
        acceptBtn.onClick.RemoveAllListeners();
        declineBtn.onClick.RemoveAllListeners();

        acceptBtn.onClick.AddListener(() => acceptCallback());
        declineBtn.onClick.AddListener(() => declineCallback());
    }

    public void SetMessageWithBtns(ServerMessage serverMessage, BtnCallback acceptCallback, BtnCallback declineCallback)
    {
        SetMessage(serverMessage, true);
        acceptBtn.onClick.RemoveAllListeners();
        declineBtn.onClick.RemoveAllListeners();

        acceptBtn.onClick.AddListener(() => acceptCallback());
        declineBtn.onClick.AddListener(() => declineCallback());
    }

    public void DefaultCallback(ServerMessage serverMessage)
    {
        if (serverMessage.IsShowMessage())
            SetMessage(serverMessage.message);

        //Debug.Log(serverMessage.message);
    }
}