using System.Collections.Generic;
using System.Threading.Tasks;
using Core.Rest;
using UnityEngine;

/*
 * Script which handles the Friendship stuff in Scenes/Examples/REST/BasicGETSET
 */
namespace MISC
{
    public class GetSetRest : MonoBehaviour
    {
        //TODO MAYBE NOT SET THEM IN CODE
        //may result in serialization erros!
        [Tooltip("Input the data in the inspector!")]
        public string username = "";

        public string lobbyName = "";
        public string inventoryName = "";
        public string guildName = "";

        public Popup popup;

        //The server calls are always the same way in this template.

        #region PlayerMethods

        public async Task GetPlayerByID(string id)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", id }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/get_player_by_id/", dataToSend, popup.DefaultCallback);
        }

        public async Task SetPlayerByID(string id)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", id },
                { "playerClass", "Stupid" }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/set_player_by_id/", dataToSend, popup.DefaultCallback);
        }

        public async Task GetAllPlayers()
        {
            await ServerCaller.Instance.GenericRequestAsync("rest/get_players/", popup.DefaultCallback);
        }

        //=============BTNCALLS==========
        public async void GetPlayer()
        {
            await GetPlayerByID(username);
        }

        public async void SetPlayer()
        {
            await SetPlayerByID(username);
        }

        public async void GetAllPlayer()
        {
            await GetAllPlayers();
        }

        #endregion

        #region LobbyMethods

        public async Task GetLobbyByID(string id)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", id }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/get_lobby_by_id/", dataToSend, popup.DefaultCallback);
        }

        //TODO
        public async Task SetLobbyByID(string id)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", id },
                { "finishSelecting", "[1,2,3,4]" },
                { "players", "[0,1,2]" }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/set_lobby_by_id/", dataToSend, popup.DefaultCallback);
        }

        public async Task GetAllLobbies()
        {
            await ServerCaller.Instance.GenericRequestAsync("rest/get_lobbies/", popup.DefaultCallback);
        }

        //=============BTNCALLS==========
        public async void GetLobby()
        {
            await GetLobbyByID(lobbyName);
        }

        public async void SetLobby()
        {
            await SetLobbyByID(lobbyName);
        }

        public async void GetAllLobby()
        {
            await GetAllLobbies();
        }

        #endregion

        #region InventoryMethods

        public async Task GetInventoryByID(string id)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", id }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/get_inventory_by_id/", dataToSend,
                popup.DefaultCallback);
        }

        public async Task SetInventoryByID(string id)
        {
            var inventoryJson =
                "{ \"name\": \"Gold\", \"type\": \"Currency\", \"quantity\": 100 }, { \"name\": \"Health Potion\", \"type\": \"Consumable\", \"effect\": \"Heals 50 HP\", \"quantity\": 3 }, { \"name\": \"Arrow\", \"type\": \"Ammunition\", \"quantity\": 50 }";

            var dataToSend = new Dictionary<string, object>
            {
                { "id", id },
                { "inventory", inventoryJson }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/set_inventory_by_id/", dataToSend,
                popup.DefaultCallback);
        }

        public async Task GetAllInventories()
        {
            await ServerCaller.Instance.GenericRequestAsync("rest/get_inventories/", popup.DefaultCallback);
        }

        //=============BTNCALLS==========
        public async void GetInventory()
        {
            await GetInventoryByID(inventoryName);
        }

        public async void SetInventory()
        {
            await SetInventoryByID(inventoryName);
        }

        public async void GetAllInventory()
        {
            await GetAllInventories();
        }

        #endregion

        #region GuildMethods

        public async Task GetGuildByID(string id)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", id }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/get_guild_by_id/", dataToSend, popup.DefaultCallback);
        }

        public async Task SetGuildByID(string id)
        {
            var dataToSend = new Dictionary<string, object>
            {
                { "id", id },
                { "guildPlayers", "[0,1,2,3]" },
                { "guildOwner", 1 }
            };
            await ServerCaller.Instance.GenericSendAsync("rest/set_guild_by_id/", dataToSend, popup.DefaultCallback);
        }

        public async Task GetAllGuilds()
        {
            await ServerCaller.Instance.GenericRequestAsync("rest/get_guilds/", popup.DefaultCallback);
        }

        //=============BTNCALLS==========
        public async void GetGuild()
        {
            await GetGuildByID(guildName);
        }

        public async void SetGuild()
        {
            await SetGuildByID(guildName);
        }

        public async void GetAllGuild()
        {
            await GetAllGuilds();
        }

        #endregion
    }
}