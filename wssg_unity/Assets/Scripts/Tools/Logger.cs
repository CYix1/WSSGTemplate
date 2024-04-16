using TMPro;
using UnityEngine;

public class Logger : MonoBehaviour
{
    public TextMeshProUGUI logText;

    // Start is called before the first frame update
    private void Start()
    {
        Application.logMessageReceived += LogCaughtException;
    }

    private void LogCaughtException(string condition, string stacktrace, LogType type)
    {
        var message = "";
        if (type == LogType.Error || type == LogType.Exception)
            message = $"<color=red>{condition}\n{stacktrace}</color>\n";
        else
            message = $"{condition}\n{stacktrace}\n";
        logText.text += message;
    }

    public void ButtonClear()
    {
        logText.text = "";
    }
}