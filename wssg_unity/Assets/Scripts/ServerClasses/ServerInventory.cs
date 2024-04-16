using System;
using System.Collections.Generic;

namespace ServerClasses
{
    /*
     * The counterpart for models.py -> Inventory
     * Every player ForeignKey is being replaced with a string to make it easier
     */
    [Serializable]
    public class ServerInventory : ServerClass
    {
        public string owner;
        public List<int> inventory;
    }
}