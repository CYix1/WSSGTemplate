using System;
using System.Collections.Generic;

namespace ServerClasses
{
    /*
     * The counterpart for models.py -> Leaderboard
     * Every player ForeignKey is being replaced with a string to make it easier
     * Little showcase if one wants to use objects instead of strings.
     */
    [Serializable]
    public class ServerChat
    {
        public string name;
        public List<Message> messages;


        //entries: [{"player": "test", "score": 42},{"player": "Max Mustermann", "score": 69}]
        public class Message
        {
            public string message;
            public DateTime time;
            public string username;


            public Message(string username, DateTime time, string message)
            {
                this.username = username;
                this.time = time;
                this.message = message;
            }
        }
    }
}