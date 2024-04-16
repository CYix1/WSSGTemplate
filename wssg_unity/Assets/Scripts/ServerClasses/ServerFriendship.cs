using System;

namespace ServerClasses
{
    /*
     * The counterpart for models.py -> Friendship
     * Every player ForeignKey is being replaced with a string to make it easier
     */
    [Serializable]
    public class ServerFriendship : ServerClass
    {
        public string personOne;
        public string personTwo;
        public int xp;
    }
}