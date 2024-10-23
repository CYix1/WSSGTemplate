/*
 * Some static settings like url, DEBUG mode or the username
 */

public static class TemplateSettings
{
    public static bool DEBUG = true;

    //every public url needs an / at the end e.g SUBDOMAIN.serveo.net/
    //public static string url = DEBUG ? "http://127.0.0.1:8000/" : "http://SUBDOMAIN_SERVEO/";
    //if using ngrok
    public static string url = DEBUG ? "http://127.0.0.1:8000/" : "http://SUBDOMAIN_NGROK/";
    //public static string url = DEBUG ? "http://127.0.0.1:8000/" : "http://SUBDOMAIN_NGROK_TCP/";


    public static string username = "";
}