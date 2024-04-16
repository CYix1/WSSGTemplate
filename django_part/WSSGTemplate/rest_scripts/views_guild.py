import json

from django.http import HttpResponse

import utilities
from ServerClass import ServerClass
from WSSGTemplate.rest_scripts import views

'''
get_guild_by_id receives: "id"
get guild by their name
'''


def get_guild_by_id(request):
    return views.get_by_id_with_communication(request, ServerClass.Guild)


'''
get_guilds receives: nothing
get all guilds 
'''


def get_guilds(request):
    return views.get_all_with_communication(request, server_class=ServerClass.Guild)


'''
set_guild_by_id receives: "id" optional: "guildPlayers", "guildOwner", "guildName"
set a guild with the given the optional keys
'''


def set_guild_by_id(request):
    result_from_check = utilities.basic_request_check(request, ["id", "guildPlayers", "guildOwner", "guildName"],
                                                      ignore_missing_values=True)
    if isinstance(result_from_check, HttpResponse):
        return result_from_check

    guild_name_req = result_from_check["id"]

    current_guild = utilities.search_object_by_attribute(ServerClass.Guild, guildName=guild_name_req)
    if current_guild is None:
        return utilities.server_message_response(message=f"No GUILD with NAME {guild_name_req} was found",
                                                 identifier="ERROR")

    extracted_values_keys = result_from_check.keys()

    warning_message = ""

    if "guildPlayers" in extracted_values_keys:
        guild_players_req = result_from_check["guildPlayers"]
        player_names = utilities.convert_ids_to_list_of_names(json.loads(guild_players_req),
                                                              server_class=ServerClass.Player)
        current_guild.guildPlayers.clear()

        for index, player_name in enumerate(player_names):

            player_instance = utilities.search_object_by_attribute(ServerClass.Player, name=player_name)
            if player_instance is None:
                warning_message += f"Player at pos {index + 1} was NOT added\n"
                continue
            current_guild.guildPlayers.add(player_instance)

    if "guildOwner" in extracted_values_keys:
        guild_owner_name_req = result_from_check["guildOwner"]
        guild_owner = utilities.search_object_by_attribute(ServerClass.Player, name=guild_owner_name_req)
        if guild_owner is None:
            return utilities.server_message_response(f"player {guild_owner_name_req} not found")
        current_guild.guildOwner = guild_owner

    if "guildName" in extracted_values_keys:
        guild_name_req = result_from_check["guildName"]
        current_guild.guildName = guild_name_req

    current_guild.save()
    return utilities.server_message_response(identifier="WARNING", message=
    f"Saved New GUILD {current_guild} \n" + ('warning:\n' + warning_message if warning_message else ''), status=200)
