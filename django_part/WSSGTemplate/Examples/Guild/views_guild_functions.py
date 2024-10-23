from django.http import HttpResponse

from WSSGTemplate.Core import utilities
from WSSGTemplate.Core.models import *
from WSSGTemplate.Examples.MISC import views


def join_guild(request):
    print("join guild")
    result_from_check = utilities.basic_request_check(request, ["id", "guildname"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    player_id = result_from_check["id"]
    guild_name = result_from_check["guildname"]

    # extract guild
    guild_obj = utilities.search_object_by_attribute(Guild, guildName=guild_name)
    print(guild_obj)
    if guild_obj is None:
        return utilities.server_message_response(message=f"no guild with name {guild_name} was found!")

    # get player object !!
    player_obj = utilities.search_object_by_attribute(Player, name=player_id)
    if player_obj is None:
        return utilities.server_message_response(message=f"no player with name {guild_name} was found!")

    # add player

    guild_obj.guildPlayers.add(player_obj)
    guild_obj.save()

    return utilities.server_message_response(message="join guild", identifier="MESSAGE", status=200)


def leave_guild(request):
    print("leave guild")
    result_from_check = utilities.basic_request_check(request, ["id", "guildname"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    player_id = result_from_check["id"]
    guild_name = result_from_check["guildname"]

    # extract guild
    guild_obj = utilities.search_object_by_attribute(Guild, guildName=guild_name)
    print(guild_obj)
    if guild_obj is None:
        return utilities.server_message_response(message=f"no guild with name {guild_name} was found!")

    # get player object !!
    player_obj = utilities.search_object_by_attribute(Player, name=player_id)
    if player_obj is None:
        return utilities.server_message_response(message=f"no player with name {player_id} was found!")

    # add player

    guild_obj.guildPlayers.remove(player_obj)
    guild_obj.save()

    return utilities.server_message_response(message="leave guild", identifier="MESSAGE", status=200)


def debug_guild(request):
    print("debug")
    # get all from view script
    model_instances = views.generic_get_all(Guild)
    # convert to json
    res = utilities.get_json_from_instances(model_instances)
    return utilities.server_message_response(status=200, identifier="MESSAGE", message=f"{res}")
