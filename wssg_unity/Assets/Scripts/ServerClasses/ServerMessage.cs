using System;
using Newtonsoft.Json.Linq;

namespace ServerClasses
{
    /*
     * The counterpart for models.py -> ServerMessage
     * Every player ForeignKey is being replaced with a string to make it easier
     * A generic structure for the messages between server and client.
     * It makes some things easier and is better than explicitly stating each return/response value in the json string.
     */
    [Serializable]
    public class ServerMessage
    {
        public string extraMessage;
        public string message;
        public string identifier;

        public ServerMessage(string extraMessage = null, string message = null, string identifier = null)
        {
            this.extraMessage = extraMessage;
            this.message = message;
            this.identifier = identifier;
        }

        public bool IsShowMessage()
        {
            return identifier.Equals("MESSAGE") || identifier.Equals("ERROR") || identifier.Equals("WARNING");
        }

        public bool IsData()
        {
            return identifier.Equals("DATA");
        }

        public override string ToString()
        {
            //THIS IS NOT SUPPORTED ON ANDROID U FUCKING BITCH
            //return JsonConvert.SerializeObject(this);
            var json = new JObject();
            json["extraMessage"] = extraMessage;
            json["message"] = message;
            json["identifier"] = identifier;

            return json.ToString();
        }

        public bool IsError()
        {
            return identifier.Equals("ERROR");
        }

        public bool IsMessage()
        {
            return identifier.Equals("MESSAGE");
        }

        public bool IsWarning()
        {
            return identifier.Equals("WARNING");
        }
    }
}