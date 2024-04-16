using System.Collections.Generic;

namespace ServerClasses
{
    /*
     * The counterpart for models.py -> Guild
     * Every player ForeignKey is being replaced with a string to make it easier
     */
    public class ServerGuild : ServerClass
    {
        public string guildName;
        public string guildOwner;
        public List<string> guildPlayers;
    }
}