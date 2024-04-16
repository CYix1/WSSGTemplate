using System;

namespace ServerClasses
{
    /*
     * Inheritance for the ServerClasses.
     * Since every authentication/validation is done via strings -> this could be unnecessary!
     */
    [Serializable]
    public abstract class ServerClass
    {
        protected int genericID; //basically a UNIQUE IDENTIFIER (UID)
    }
}