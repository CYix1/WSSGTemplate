from WSSGTemplate.Core import utilities
from WSSGTemplate.Core.Websocket.consumers_basic_layer import BasicWSServerLayer
from WSSGTemplate.Core.models import *

'''
Mostly copy pasted form WSSGTemplate/rest_scripts/views_TTT.py 
as well as the comments!
all search_object_by_attribute are changed to the async variant!
and the routing/mapping from "url" to method is done via the self.commands dictionary.

since django provides a broadcasting method to all connecting clients,
we don't need an update loop to request the newest data
but can just broadcast the changes/the newest data directly in the respective method
=>from the rest script:
update_TTTGame and get_game got merged
and end_game send a broadcast
'''


class TTTWSGame(BasicWSServerLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.commands = {
            "CREATE GAME": self.handle_create,
            "UPDATE GAME": self.handle_update_game,
            "SURRENDER GAME": self.handle_surrender_game,
            "END GAME": self.handle_end_game,
            "DEBUG": self.handle_debug,
        }

    async def handle_create(self, data):

        lobby = await utilities.asearch_object_by_attribute(Lobby, lobbyID=data["lobbyId"])
        if lobby is None:
            await self.send_message_to_client(identifier="ERROR", message="lobby somehow not found")
            return

        host = await utilities.asearch_object_by_attribute(Player, name=data["host"])
        if host is None:
            await self.send_message_to_client(identifier="ERROR", message="the host player could not be found")
            return

        opponent = await utilities.asearch_object_by_attribute(Player, name=data["opponent"])
        if opponent is None:
            await self.send_message_to_client(identifier="ERROR", message="the opponent player could not be found")
            return

        game = await  utilities.asearch_object_by_attribute(TTTGame, lobby__lobbyID=data["lobbyId"])
        if game is None:
            game = TTTGame(lobby=lobby, host=host, opponent=opponent)
            print("created lobby")
        game.save()
        await self.send_message_to_client(identifier="NOTHING", message="created game on server")

    async def handle_update_game(self, data):
        print(data)
        lobby = await utilities.asearch_object_by_attribute(Lobby, lobbyID=data["lobbyId"])
        if lobby is None:
            await self.send_message_to_client(identifier="ERROR", message="lobby somehow not found")
            return

        host = await utilities.asearch_object_by_attribute(Player, name=data["host"])
        if host is None:
            await self.send_message_to_client(identifier="ERROR", message="the host player could not be found")
            return

        opponent = await utilities.asearch_object_by_attribute(Player, name=data["opponent"])
        if opponent is None:
            await self.send_message_to_client(identifier="ERROR", message="the opponent player could not be found")
            return

        current_game = await utilities.asearch_object_by_attribute(TTTGame, lobby__lobbyID=data["lobbyId"])
        if current_game is None:
            await self.send_message_to_client(identifier="ERROR", message="GAME NOT FOUND????")
            return

        current_game.current_index = data["current_index"]

        current_game.action = json.loads(data["field"])
        current_game.save()

        json_ret = utilities.get_json_from_instance(current_game)
        json_ret["host"] = data["host"]
        json_ret["opponent"] = data["opponent"]
        json_ret["lobby"] = current_game.lobby.lobbyID
        json_ret["action"] = str(json_ret["action"])

        await self.send_broadcast_message(identifier="DATA", extra_message="gameData", message=str(json_ret))

    async def handle_end_game(self, data):

        lobby = await utilities.asearch_object_by_attribute(Lobby, lobbyID=data["lobbyId"])
        if data["playerWon"] == "DRAW":
            lobby.winner = None
        else:
            lobby.winner = await utilities.asearch_object_by_attribute(Player, name=data["playerWon"])
        lobby.isActive = False
        lobby.save()

        game = await utilities.asearch_object_by_attribute(TTTGame, lobby__lobbyID=lobby.lobbyID)
        if game is not None:
            game.delete()
        if data["playerWon"] == "DRAW":
            await self.send_broadcast_message(message=f"DRAW NO WON", identifier="MESSAGE")
        else:
            if lobby.winner is None:
                await self.send_broadcast_message(message=f"Game Terminated", identifier="MESSAGE")
            else:
                await self.send_broadcast_message(message=f"Player {lobby.winner.name} won", identifier="MESSAGE")

    async def handle_surrender_game(self, data):

        lobby = await utilities.asearch_object_by_attribute(Lobby, lobbyID=data["lobbyId"])
        if lobby is not None:

            game = await utilities.asearch_object_by_attribute(TTTGame, lobby__lobbyID=lobby.lobbyID)
            if game is not None:
                game.delete()
            lobby.delete()

        await self.send_broadcast_message(message=f"Game Terminated", identifier="MESSAGE")

    async def handle_debug(self, data):
        print("DEBUG TIME")
        await self.send_broadcast_message(message=f"TEST", identifier="MESSAGE")
