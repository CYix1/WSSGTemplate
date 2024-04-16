using System;
using Newtonsoft.Json.Linq;

namespace ServerClasses
{
    /*
     * The counterpart for models.py -> Lobby
     * Every player ForeignKey is being replaced with a string to make it easier
     */
    [Serializable]
    public class ServerTTTGame
    {
        public string action;
        public int current_index;
        public string host;
        public string lobby;
        public string opponent;

        public override string ToString()
        {
            var json = new JObject();
            json["action"] = action;
            json["current_index"] = current_index;
            json["host"] = host;
            json["lobby"] = lobby;
            json["opponent"] = opponent;

            return json.ToString();
        }
    }
}