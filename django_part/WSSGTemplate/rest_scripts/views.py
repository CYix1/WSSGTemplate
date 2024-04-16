from django.http import HttpResponse

import utilities
from ServerClass import ServerClass
from WSSGTemplate.models import *

# TODO instead of getting the response, it should only get the model and then an wrapper to get the json

'''
a generic method to get some specific object by their id
mostly getting the model and converting it into json
id= for identification
server_class = which class should be used?
'''


def generic_get_by_id(id_input, server_class):
    model_instance = None

    if server_class == server_class.Player:

        model_instance = utilities.search_object_by_attribute(ServerClass.Player, name=id_input)

    elif server_class == server_class.Lobby:
        model_instance = utilities.search_object_by_attribute(ServerClass.Lobby, lobbyID=id_input)

    elif server_class == server_class.Inventory:
        model_instance = utilities.search_object_by_attribute(ServerClass.Inventory, owner__name=id_input)

    # could use genericID, but it is more intuitive if personOne and personTwo as keys are being used
    # elif server_class == server_class.Friendship:
    #    model_instance = utilities.search_object_by_attribute(ServerClass.Friendship, genericID=id)

    # could use genericID, but it is more intuitive if requestor and receiver as keys are being used
    # elif server_class == server_class.FriendRequest:
    #    model_instance = utilities.search_object_by_attribute(ServerClass.FriendRequest, genericID=id)

    elif server_class == server_class.TTTGame:
        model_instance = utilities.search_object_by_attribute(ServerClass.TTTGame, lobby__lobbyID=id_input)

    elif server_class == server_class.Guild:
        model_instance = utilities.search_object_by_attribute(ServerClass.Guild, guildName=id_input)

    # not really intended for single get
    # elif server_class == server_class.ServerMessage:
    #    model_instance = utilities.search_object_by_attribute(ServerClass.ServerMessage, genericID=id)

    elif server_class == server_class.Leaderboard:
        model_instance = utilities.search_object_by_attribute(ServerClass.Leaderboard, category=id_input)

    return model_instance


# basic generic method to reduce code size, since it always works in the same way
# used for setting an object according to the given json string

def generic_set_by_id(dict_values, server_class):
    model_instance = generic_get_by_id(dict_values["id"], server_class)
    if model_instance is None:
        return utilities.server_message_response(message=f'no object was found with id: {dict_values["id"]}')

    model_instance = utilities.jsondict_to_obj(model_instance, dict_values)

    model_instance.save()
    return utilities.server_message_response(status=200, identifier="MESSAGE",
                                             message=f'Object {server_class} was saved or updated')


# basic generic method to reduce code size, since it always works in the same way
# used for getting  ALL objects of a class
def generic_get_all(server_class):
    model_mapping = {
        server_class.Player: Player,
        server_class.Friendship: Friendship,
        server_class.FriendRequest: FriendRequest,
        server_class.Inventory: Inventory,
        server_class.Lobby: Lobby,
        server_class.TTTGame: TTTGame,
        server_class.Guild: Guild,
        server_class.ServerMessage: ServerMessage,
        server_class.Leaderboard: Leaderboard
    }
    model_instances = model_mapping.get(server_class)
    if model_instances is not None:
        model_instances = model_instances.objects.all()

    return model_instances


def get_by_id_with_communication(request, server_class):
    result_from_check = utilities.basic_request_check(request, ["id"])

    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    id_req = result_from_check["id"]

    model_instance = generic_get_by_id(id_req, server_class=server_class)
    if model_instance is None:
        return utilities.server_message_response(f"instance of {server_class} {id_req} not found")
    else:
        result = utilities.convert_specific_fields(utilities.get_json_from_instance(model_instance))
        print(result)
        return utilities.server_message_response(status=200, identifier="MESSAGE",
                                                 message=f"{result}")


def get_all_with_communication(request, server_class):
    result_from_check = utilities.basic_request_check(request)
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    model_instances = generic_get_all(server_class=server_class)
    res = utilities.get_json_from_instances(model_instances)

    return utilities.server_message_response(status=200, identifier="MESSAGE", message=f"{res}")
