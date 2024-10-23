from django.http import HttpResponse

from WSSGTemplate.Core import utilities
from WSSGTemplate.Core.models import *
from WSSGTemplate.Examples.MISC import views

'''
get_player_by_id receives: "id"
get player by their name
'''


def get_player_by_id(request):
    return views.get_by_id_with_communication(request, Player)


'''
get_players receives: nothing
get all players 
'''


def get_players(request):
    return views.get_all_with_communication(request, Player)


'''
set_player_by_id receives: "id" optional: "name", "playerClass", "guild"
set a player with the given the optional keys
'''


def set_player_by_id(request):
    result_from_check = utilities.basic_request_check(request, ["id", "name", "playerClass", "guild"], True)
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    id_req = result_from_check["id"]

    extracted_values_keys = result_from_check.keys()

    player_instance = utilities.search_object_by_attribute(Player, name=id_req)

    if "name" in extracted_values_keys:
        name_req = result_from_check["name"]
        player_instance.name = name_req

    if "playerClass" in extracted_values_keys:
        playerClass_req = result_from_check["playerClass"]

        player_instance.playerClass = playerClass_req
    if "guild" in extracted_values_keys:
        guild_req = result_from_check["guild"]

        guild = utilities.search_object_by_attribute(Guild, guildName=guild_req)
        if guild is None:
            return utilities.server_message_response(f"guild {guild_req} not found")
        player_instance.guild = guild
    player_instance.save()
    return utilities.server_message_response(message="updated player", status=200, identifier="MESSAGE")
