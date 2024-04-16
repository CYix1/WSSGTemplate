import json

from django.http import HttpResponse

import utilities
from ServerClass import ServerClass
from WSSGTemplate.models import TTTGame

'''
end_game receives: "lobbyId", "playerWon"
sets the lobby(lobbyId) to inactive, sets the player of lobby(lobbyId) and deletes the TTTGame
'''

def surrender_game(request):
    result_from_check = utilities.basic_request_check(request, ["lobbyId"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    lobby_id_req = result_from_check["lobbyId"]
    lobby = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyID=lobby_id_req)
    if lobby is not None:

        game = utilities.search_object_by_attribute(ServerClass.TTTGame, lobby__lobbyID=lobby.lobbyID)
        if game is not None:
            game.delete()
        lobby.delete()
    return utilities.server_message_response(message=f"Game was terminated", status=200,identifier="MESSAGE")

def end_game(request):
    result_from_check = utilities.basic_request_check(request, ["lobbyId", "playerWon"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    lobby_id_req = result_from_check["lobbyId"]
    player_won_req = result_from_check["playerWon"]
    lobby = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyID=lobby_id_req)
    if lobby is None:
        return utilities.server_message_response(message=f"Lobby somehow not found")

    if player_won_req == "DRAW":
        lobby.winner = None
    else:
        player_won = utilities.search_object_by_attribute(ServerClass.Player, name=player_won_req)
        if player_won is None:
            return utilities.server_message_response(message=f"Player {player_won_req} not found")
        lobby.winner = player_won
    lobby.isActive = False
    lobby.save()

    game = utilities.search_object_by_attribute(ServerClass.TTTGame, lobby__lobbyID=lobby.lobbyID)
    game.delete()

    return utilities.server_message_response(message=f"Player {lobby.winner.name} won", status=200,
                                             identifier="MESSAGE")


'''
create_TTTGame receives: "lobbyId", "host", "opponent"
creates an TTTGame(lobbyId) with the host and opponent set
'''


def create_TTTGame(request):
    result_from_check = utilities.basic_request_check(request, ["lobbyId", "host", "opponent"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    lobby_id_req = result_from_check["lobbyId"]
    host_req = result_from_check["host"]
    opponent_req = result_from_check["opponent"]

    lobby = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyID=lobby_id_req)
    if lobby is None:
        return utilities.server_message_response(message="lobby somehow not found")
    host = utilities.search_object_by_attribute(ServerClass.Player, name=host_req)
    if host is None:
        return utilities.server_message_response(message="the host player could not be found")
    opponent = utilities.search_object_by_attribute(ServerClass.Player, name=opponent_req)
    if opponent is None:
        return utilities.server_message_response(message="the opponent player could not be found")

    game = utilities.search_object_by_attribute(ServerClass.TTTGame, lobby__lobbyID=lobby_id_req)
    if game is None:
        game = TTTGame(lobby=lobby, host=host, opponent=opponent)

    game.save()
    return utilities.server_message_response(status=200, identifier="NOTHING", message="created game on server")


'''
update_TTTGame receives: "lobbyId", "host", "opponent", "field", "current_index"
updates the TTTGame according to the fields.
TODO: either replace with a generic set or perform some checks 
'''


def update_TTTGame(request):
    result_from_check = utilities.basic_request_check(request,
                                                      ["lobbyId", "host", "opponent", "field", "current_index"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check

    lobby_id_req = result_from_check["lobbyId"]
    host_req = result_from_check["host"]
    opponent_req = result_from_check["opponent"]
    field_req = result_from_check["field"]
    current_index = result_from_check["current_index"]

    lobby = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyID=lobby_id_req)
    if lobby is None:
        return utilities.server_message_response(message="lobby somehow not found")
    host = utilities.search_object_by_attribute(ServerClass.Player, name=host_req)
    if host is None:
        return utilities.server_message_response(message="the host player could not be found")
    opponent = utilities.search_object_by_attribute(ServerClass.Player, name=opponent_req)
    if opponent is None:
        return utilities.server_message_response(message="the opponent player could not be found")

    current_game = TTTGame.objects.get(lobby__lobbyID=lobby_id_req)
    if current_game is None:
        return utilities.server_message_response(message="GAME NOT FOUND????")

    current_game.current_index = current_index

    current_game.action = json.loads(field_req)
    current_game.save()
    return utilities.server_message_response(identifier="NOTHING", message="updated field in server", status=200)


'''
get_game receives: "lobbyId", "host", "opponent"
returns a readable string for the client of a TTTGame

TODO: replace with a generic get?
'''


def get_game(request):
    result_from_check = utilities.basic_request_check(request, ["lobbyId", "host", "opponent"])

    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    lobby_id_req = result_from_check["lobbyId"]
    host_req = result_from_check["host"]
    opponent_req = result_from_check["opponent"]

    current_lobby = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyID=lobby_id_req)
    if current_lobby is None:
        return utilities.server_message_response(message=f"Lobby with {lobby_id_req} not found")

    if current_lobby.winner is not None:
        return utilities.server_message_response(message=f"Player {current_lobby.winner.name} won", status=200,
                                                 identifier="MESSAGE")
    current_game = utilities.search_object_by_attribute(ServerClass.TTTGame, lobby__lobbyID=lobby_id_req)
    if current_game is None:
        if current_lobby.winner is None and current_lobby.isActive is False:
            return utilities.server_message_response(message=f"Match was terminated either Draw or surrender!")

        return utilities.server_message_response(
            message=f"game with {host_req} and {opponent_req} not found", identifier="WARNING")

    json_ret = utilities.get_json_from_instance(current_game)

    json_ret["host"] = host_req
    json_ret["opponent"] = opponent_req
    json_ret["lobby"] = current_game.lobby.lobbyID
    json_ret["action"] = str(json_ret["action"])
    return utilities.server_message_response(message=str(json_ret), status=200, identifier="DATA")
