using System;

namespace ServerClasses
{
    /*
     * The counterpart for models.py -> Lobby
     * Every player ForeignKey is being replaced with a string to make it easier
     */
    [Serializable]
    public class ServerPlayer : ServerClass
    {
        public string user;
        public string name = "anonymous";
        public string player_class = "none";
        public ServerGuild guild;
    }
}