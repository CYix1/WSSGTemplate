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
    public class ServerLeaderboard
    {
        public string category;
        public List<Entry> entries;


        //entries: [{"player": "test", "score": 42},{"player": "Max Mustermann", "score": 69}]
        public class Entry
        {
            public string player;
            public int score;

            public Entry(string player = null, int score = default)
            {
                this.player = player;
                this.score = score;
            }
        }
    }
}