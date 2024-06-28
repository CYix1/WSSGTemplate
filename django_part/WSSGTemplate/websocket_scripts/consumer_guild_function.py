from asgiref.sync import sync_to_async

import utilities
from ServerClass import ServerClass
from WSSGTemplate.models import *
from WSSGTemplate.websocket_scripts.consumers_basic_layer import BasicWSServerLayer


class WSGuildfunction(BasicWSServerLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.commands = {
            "join": self.handle_join,
            "leave": self.handle_leave,
            "debug": self.handle_debug,
        }

    async def handle_join(self, data):

        player_id = data["id"]
        guild_name = data["guildname"]

        #get guild object
        guild_obj = await  utilities.asearch_object_by_attribute(ServerClass.Guild, guildName=guild_name)
        if guild_obj is None:
            await self.send_broadcast_message(message=f"no guild with name {guild_name} was found!", identifier="ERROR")
            return

        #get player object
        player_obj = await  utilities.asearch_object_by_attribute(ServerClass.Player, name=player_id)
        if player_obj is None:
            await self.send_broadcast_message(message=f"no player with name {player_id} was found!", identifier="ERROR")
            return

        #add player
        guild_obj.guildPlayers.add(player_obj)
        guild_obj.save()

        await self.send_broadcast_message(message="Added player to guild", identifier="MESSAGE")

    async def handle_leave(self, data):
        player_id = data["id"]
        guild_name = data["guildname"]

        # get guild object
        guild_obj = await  utilities.asearch_object_by_attribute(ServerClass.Guild, guildName=guild_name)
        if guild_obj is None:
            await self.send_broadcast_message(message=f"no guild with name {guild_name} was found!", identifier="ERROR")
            return

        # get player object
        player_obj = await  utilities.asearch_object_by_attribute(ServerClass.Player, name=player_id)
        if player_obj is None:
            await self.send_broadcast_message(message=f"no player with name {player_id} was found!", identifier="ERROR")
            return

        # add player
        guild_obj.guildPlayers.remove(player_obj)
        guild_obj.save()

        await self.send_broadcast_message(message="removed player to guild", identifier="MESSAGE")


    async def handle_debug(self, data):
        print(data)
        model_instances = await sync_to_async(list)(Guild.objects.all())
        res = utilities.get_json_from_instances(model_instances)

        await self.send_broadcast_message(message=f"{res}", identifier="MESSAGE")
