using System;
using System.Collections.Generic;

namespace ServerClasses
{
    /*
     * The counterpart for models.py -> Lobby
     * Every player ForeignKey is being replaced with a string to make it easier
     */
    [Serializable]
    public class ServerLobby : ServerClass
    {
        public string lobbyID;
        public List<string> players;
        public List<int> finishSelecting;
        public bool isActive;
        public bool startGame;
        public string winner;
    }
}