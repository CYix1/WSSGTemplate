from WSSGTemplate.Core import utilities
from WSSGTemplate.Core.Websocket.consumers_basic_layer import BasicWSServerLayer
from WSSGTemplate.Core.models import *

'''
Mostly copy pasted form parts of WSSGTemplate/rest_scripts/views_lobby.py 
as well as the comments!
all search_object_by_attribute are changed to the async variant!
and the routing/mapping from "url" to method is done via the self.commands dictionary.

since django provides a broadcasting method to all connecting clients, we don't need an update loop to request the newest data
but can just broadcast the changes/the newest data directly in the respective method

join_lobby from the rest script 
is being done with a broadcast in handle_join
since it basically tells both clients that the amount of players should be 2 => switch scene
'''


class TTTWSLobby(BasicWSServerLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.commands = {
            "CREATE LOBBY": self.handle_create,
            "JOIN LOBBY": self.handle_join,
            "START LOBBY": self.handle_start_lobby,
            "DEBUG": self.handle_debug,

        }

    async def handle_debug(self, data):
        print("DEBUG TIME")
        await self.send_broadcast_message(message=f"TEST", identifier="MESSAGE")

    async def handle_create(self, data):

        player = await utilities.asearch_object_by_attribute(Player, name=data["host"])

        if player is None:
            await self.send_message_to_client(message="No user with this name found")
            return

        current_lobby = await utilities.asearch_object_by_attribute(Lobby, lobbyID=data["id"])
        if current_lobby is None:
            current_lobby = Lobby(lobbyID=data["id"])
            # see https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_many/
            # need to save the lobby before setting many to many relationships
            current_lobby.save()
        elif current_lobby.players.first() is not player:
            await self.send_message_to_client(
                message=f"There already exists an lobby with this name, with another host({current_lobby.players.first()})! ")
            return
        current_lobby.players.clear()
        current_lobby.players.add(player)

        current_lobby.save()
        await self.send_broadcast_message(identifier="DATA", extra_message="lobbyData",
                                          message=utilities.get_readable_lobby_json(current_lobby))

    async def handle_join(self, data):
        player = await utilities.asearch_object_by_attribute(Player, name=data["id"])
        if player is None:
            await self.send_message_to_client(message="palyer not found")
            return
        current_lobby = await utilities.asearch_object_by_attribute(Lobby, lobbyID=data["lobbyId"])
        if current_lobby is None:
            await self.send_message_to_client(message="lobby not found")
            return
        current_lobby.players.add(player)
        current_lobby.save()

        await self.send_broadcast_message(identifier="DATA", extra_message="lobbyData",
                                          message=utilities.get_readable_lobby_json(current_lobby))

    async def handle_start_lobby(self, data):

        current_lobby = await  utilities.asearch_object_by_attribute(Lobby, lobbyID=data["id"])
        if current_lobby is None:
            await self.send_message_to_client(message="lobby not found")
            return
        current_lobby.startGame = data["startGame"]
        current_lobby.save()
        await self.send_message_to_client(identifier="MESSAGE", message="START Lobby")

    async def handle_get_lobby(self, data):
        current_lobby = await utilities.asearch_object_by_attribute(Lobby, lobbyID=data["id"])

        if current_lobby is None:
            await self.send_message_to_client(message="lobby not found")
            return
        result = utilities.convert_specific_fields(utilities.get_json_from_instance(current_lobby))

        result["players"] = utilities.convert_ids_to_list_of_names(result["players"], Player)
        result = utilities.convert_specific_fields(result)
        await self.send_message_to_client(identifier="DATA", extra_message="lobbyData", message=str(result))
