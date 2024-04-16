using System;

namespace ServerClasses
{
    /*
     * The counterpart for models.py -> FriendRequest
     * Every player ForeignKey is being replaced with a string to make it easier
     */
    [Serializable]
    public class ServerFriendRequest : ServerClass
    {
        public string requestor;
        public string receiver;
        public bool accepted;
    }
}