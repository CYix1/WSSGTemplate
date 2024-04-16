from django.http import HttpResponse

import utilities
from ServerClass import ServerClass
from WSSGTemplate.models import Lobby
from WSSGTemplate.rest_scripts import views

'''
get_lobby_by_id receives: "id"
get lobby by the lobbyID/ lobbyName
'''


def get_lobby_by_id(request):
    result_from_check = utilities.basic_request_check(request, ["id"])

    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    id_req = result_from_check["id"]

    model_instance = views.generic_get_by_id(id_req, server_class=ServerClass.Lobby)
    if model_instance is None:
        return utilities.server_message_response(message="NO lobby found")
    return utilities.server_message_response(
        message=utilities.get_readable_lobby_json(model_instance), status=200,
        identifier="DATA")


'''
get_lobbies receives: nothing
get all lobbies great for some quick join functionality! 
'''


def get_lobbies(request):
    return views.get_all_with_communication(request, server_class=ServerClass.Lobby)


'''
set_lobby_by_id receives: "id" optional: "players", "finishSelecting", "isActive", "startGame", "winner"
set a lobby with the given the optional keys
'''


def set_lobby_by_id(request):
    # basic check
    result_from_check = utilities.basic_request_check(request,
                                                      ["id", "players", "finishSelecting", "isActive", "startGame",
                                                       "winner"], ignore_missing_values=True)
    if isinstance(result_from_check, HttpResponse):
        return result_from_check

    # extract values
    print(result_from_check)
    extracted_values_key = result_from_check.keys()
    id_req = result_from_check["id"]
    # get current lobby
    current_lobby = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyID=id_req)
    if current_lobby is None:
        return utilities.server_message_response(f"No Lobby with ID {id_req} was found")

    current_lobby.save()

    updated_field = ""

    # lobby.players is a MANY TO MANY FIELD: Therefore we need to singly add all players to this list. otherwise there could be an error.
    # For that we can convert all IDS to the player names and search by them to get the instance
    # TODO try it with genericID, no converting to names
    if "players" in extracted_values_key:
        player_names_req = result_from_check["players"]

        current_lobby.players.clear()
        warning_message = ""

        for index, player_id in enumerate(player_names_req):
            player_instance = utilities.search_object_by_attribute(ServerClass.Player, genericID=player_id)
            if player_instance is None:
                warning_message += f"Player at pos {index + 1} was NOT added\n"
                continue
            current_lobby.players.add(player_instance)

        updated_field += " player "

    if "finishSelecting" in extracted_values_key:
        finish_selecting_req = result_from_check["finishSelecting"]
        current_lobby.finishSelecting = finish_selecting_req
        updated_field += " finishSelecting "

    if "isActive" in extracted_values_key:
        is_active_req = result_from_check["isActive"]
        current_lobby.isActive = is_active_req
        updated_field += " isActive "

    if "startGame" in extracted_values_key:
        start_game_req = result_from_check["startGame"]
        current_lobby.isActive = start_game_req
        updated_field += " startGame "

    if "winner" in extracted_values_key:
        winner_req = result_from_check["winner"]
        current_lobby.winner = winner_req
        updated_field += " winner "

    current_lobby.save()
    result = utilities.convert_specific_fields(utilities.get_json_from_instance(current_lobby))
    return utilities.server_message_response(message=result, identifier="DATA", status=200)


'''
create_lobby receives: "id", "host"
creates a lobby with the host being the FIRST player added to Lobby.players if host is removed. the NEXT in Lobby.players will be the next host
'''


def create_lobby(request):
    result_from_check = utilities.basic_request_check(request, ["host", "id"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check

    id_req = result_from_check["id"]
    host_req = result_from_check["host"]

    player = utilities.search_object_by_attribute(ServerClass.Player, name=host_req)

    if player is None:
        return utilities.server_message_response(message="player was not found")

    current_lobby = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyID=id_req)

    if current_lobby is None:
        current_lobby = Lobby(lobbyID=id_req)
        # see https://docs.djangoproject.com/en/5.0/topics/db/examples/many_to_many/
        # need to save the lobby before setting many to many relationships
        current_lobby.save()
    # if lobby is inactive nice, active wrong TODO
    elif current_lobby.players.first() is not player and current_lobby.isActive == True:
        return utilities.server_message_response(
            message=f"There already exists an lobby with this name, with another host({current_lobby.players.first()})! ")

    current_lobby.players.clear()
    current_lobby.players.add(player)

    current_lobby.save()

    return utilities.server_message_response(message="Lobby was created", identifier="NOTHING", status=200)


'''
delete_lobby_by_id receives: "id"
deletes a lobby by id
'''


def delete_lobby_by_id(request):
    result_from_check = utilities.basic_request_check(request, ["id"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    id_req = result_from_check["id"]

    current_lobby = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyId=id_req)
    if current_lobby is None:
        return utilities.server_message_response(message="Lobby didn't exits. OK", identifier="NOTHING", status=200)

    current_lobby.delete()
    return utilities.server_message_response(message="Lobby was deleted successfully", identifier="NOTHING", status=200)


'''
join_lobby receives: "id", "lobbyId"
user(is) joins a lobby(lobbyId)
'''


def join_lobby(request):
    result_from_check = utilities.basic_request_check(request, ["id", "lobbyId"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    id_req = result_from_check["id"]
    lobby_id_req = result_from_check["lobbyId"]

    player = utilities.search_object_by_attribute(ServerClass.Player, name=id_req)
    if player is None:
        return utilities.server_message_response(message="player was not found")

    current_lobby = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyID=lobby_id_req)

    if current_lobby is None:
        return utilities.server_message_response(message="lobby not found")

    current_lobby.players.add(player)
    current_lobby.save()

    return utilities.server_message_response(
        message=utilities.get_readable_lobby_json(current_lobby), status=200,
        identifier="DATA")
