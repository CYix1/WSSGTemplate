using System.Collections.Generic;
using System.Threading.Tasks;
using MISC;
using Newtonsoft.Json;
using ServerClasses;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

/*
 * Script which handles the Friendship stuff in Scenes/Examples/REST/Friendship
 */
namespace Core.Rest.Friendship
{
    public class FriendShipUI : MonoBehaviour
    {
        //Two different content of scroll views
        [Header("Contents")] public GameObject FriendListContent;

        public GameObject FriendRequestContent;

        //Two different prefab for scroll views
        [Header("Prefabs")] public GameObject FriendListItemPrefab;

        public GameObject FriendRequestItemPrefab;


        [Header("Other")] public TMP_InputField FriendRequestInput;

        public TextMeshProUGUI usernameLabel;
        public Popup popup;


        private List<ServerFriendRequest> serverFriendRequests = new();
        private List<ServerFriendship> serverFriendships = new();


        private async void Start()
        {
            //display the user's name
            usernameLabel.text = TemplateSettings.username;

            //reset the UI by destroying all items.
            foreach (Transform VARIABLE in FriendListContent.transform) Destroy(VARIABLE.gameObject);
            foreach (Transform VARIABLE in FriendRequestContent.transform) Destroy(VARIABLE.gameObject);

            //servercalls
            await RequestFriendShipData();
            await RequestFriendRequestData();
        }

        public void Refresh()
        {
            Start();
        }


        /*
         * Generates the UI for the friendship scene, according to the serverFriendships attribute
         */
        public void GenerateFriendListUI()
        {
            for (var i = 0; i < serverFriendships.Count; i++)
            {
                var itemUIobj = Instantiate(FriendListItemPrefab, FriendListContent.transform);
                var label = itemUIobj.GetComponentInChildren<TextMeshProUGUI>();
                var othersName = TemplateSettings.username.Equals(serverFriendships[i].personOne)
                    ? serverFriendships[i].personTwo
                    : serverFriendships[i].personOne;
                label.text = othersName;

                var btn = itemUIobj.GetComponentInChildren<Button>();
                btn.onClick.AddListener(() => RemoveFriend(othersName, itemUIobj));
            }
        }

        /*
         * Generates the UI for the friendship scene, according to the serverFriendships attribute
         */
        public void GenerateFriendRequestsUI()
        {
            for (var i = 0; i < serverFriendRequests.Count; i++)
            {
                var itemUIobj = Instantiate(FriendRequestItemPrefab, FriendRequestContent.transform);
                var label = itemUIobj.GetComponentInChildren<TextMeshProUGUI>();
                label.text = "" + serverFriendRequests[i].requestor;
                var btns = itemUIobj.GetComponentsInChildren<Button>();

                // this line is needed since the scope is different for the calls.
                // if removed, it will result in X buttons doing the same thing (for index serverFriendRequests.Count-1)
                var index = i;
                btns[0].onClick
                    .AddListener(() => AcceptFriendRequest(serverFriendRequests[index].requestor, itemUIobj));
                btns[1].onClick
                    .AddListener(() => DeclineFriendRequest(serverFriendRequests[index].requestor, itemUIobj));
            }
        }

        //return value is from the server, so I know that the result (if successful) is a List of ServerFriendRequest
        public void SetFriendRequestsDataFromServer(ServerMessage serverMessage)
        {
            if (serverMessage.identifier.Equals("ERROR"))
                return;

            serverFriendRequests = JsonConvert.DeserializeObject<List<ServerFriendRequest>>(serverMessage.message);
            GenerateFriendRequestsUI();
        }


        //return value is from the server, so I know that the result (if successful) is a List of ServerFriendship
        public void SetFriendShipDataFromServer(ServerMessage serverMessage)
        {
            if (serverMessage.identifier.Equals("ERROR"))
                return;

            serverFriendships = JsonConvert.DeserializeObject<List<ServerFriendship>>(serverMessage.message);
            GenerateFriendListUI();
        }

        #region ServerCalls

        //The different server calls needed for this scene.    
        private async void RemoveFriend(object playerID, GameObject btn)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "friendID", playerID }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/remove_friend/", dataToSend, popup.DefaultCallback);

            Destroy(btn);
            Refresh();
        }

        private async void AcceptFriendRequest(object playerID, GameObject btn)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "friendID", playerID }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/accept_friend_request/", dataToSend,
                popup.DefaultCallback);
            Destroy(btn);
            Refresh();
        }

        private async void DeclineFriendRequest(object playerID, GameObject btn)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "friendID", playerID }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/remove_friend_request/", dataToSend,
                popup.DefaultCallback);

            Destroy(btn);
            Refresh();
        }

        public async void CreateFriendRequest()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username },
                { "friendID", FriendRequestInput.text }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/create_friend_request/", dataToSend,
                popup.DefaultCallback);
        }

        //other callback!
        public async Task RequestFriendRequestData()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/get_friend_receives/", dataToSend,
                SetFriendRequestsDataFromServer);
        }

        //other callback!
        public async Task RequestFriendShipData()
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", TemplateSettings.username }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/get_all_friendsships/", dataToSend,
                SetFriendShipDataFromServer);
        }

        #endregion
    }
}