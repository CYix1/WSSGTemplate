from typing import Any
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse

from ServerClass import ServerClass
from WSSGTemplate.models import *

'''
depending on the format for the data send to the server. returns the varialbe if existing
'''


def extract_request_value(request, variable_name):
    try:
        content_type = request.content_type.lower()

        if 'application/json' in content_type:
            post_data = json.loads(request.body)
            return post_data.get(variable_name)
        elif 'application/x-www-form-urlencoded' in content_type:
            post_data = parse_qs(request.body.decode("utf-8"))
            return post_data.get(variable_name, [])[0]
    except Exception as e:
        print("variable_name is probably wrong or it doesn't exist! error for:" + variable_name)
        print(e)
        return None


'''
same as before just as a dictionary
'''


def extract_request_values(request):
    try:
        content_type = request.content_type.lower()
        data = {}

        if 'application/json' in content_type:
            post_data = json.loads(request.body)
            data.update(post_data)
        elif 'application/x-www-form-urlencoded' in content_type:
            post_data = parse_qs(request.body.decode("utf-8"))
            for key, value in post_data.items():
                data[key] = value[0]

        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# generic method to set the variables depending on a dictionary in json format
def jsondict_to_obj(model_instance, json_dic):
    for key, value in json_dic.items():
        if hasattr(model_instance, key):
            field = getattr(model_instance, key)
            print(model_instance, field, key, value)
            # TODO what about ForeignKeys or ManyToMany?
            setattr(model_instance, key, value)
        else:
            print(f"K: {key} V:{value} could not be set! Does the attribute {key} exists?")
    return model_instance


# convert genericID of model to a more userfriendly thing mostly their name
def convert_server_class_id_to_name(id_input, server_class) -> str | None:
    attribute_mappings = {
        ServerClass.Player: 'name',
        ServerClass.Lobby: 'lobbyID',
        ServerClass.Inventory: 'owner__name',
        ServerClass.Guild: 'guildName',
    }

    attribute = attribute_mappings.get(server_class)
    if attribute is None:
        return None

    model_instance = search_object_by_attribute(server_class, genericID=id_input)
    if model_instance is None:
        return None

    return getattr(model_instance, attribute)


def convert_ids_to_list_of_names(ids, server_class) -> list | None:
    result = []
    for id_input in ids:
        temp_name = convert_server_class_id_to_name(id_input, server_class)
        if temp_name is None:
            print("NONONONO")
        result.append(temp_name)
    return result


'''
identifier, usage                   status code
MESSAGE - display in e.g. popup -   200
DATA    - use the data somehow  -   200
NOTHING - ignorable messages    -   200
ERROR   - error                 -   400
WARNING - warning               -   200
'''


# default is set to ERROR message
def server_message_response(message, identifier="ERROR", extra_message="server", status=400):
    # ServerMessages are also available as models if one wants to use the messages as data for something
    return HttpResponse(server_message_json(message=message, identifier=identifier, extra_message=extra_message),
                        status=status)


# json representation
def server_message_json(message, identifier="ERROR", extra_message="server"):
    return json.dumps({
        "extraMessage": extra_message,
        "message": message,
        "identifier": identifier
    })


# detailed view to print a class
def print_out(my_instance):
    # Print out attributes and   methods
    print("Attributes:")
    for attribute_name in dir(my_instance):
        attribute_value = getattr(my_instance, attribute_name)
        if not callable(attribute_value):
            print(f"{attribute_name}: {attribute_value}")

    print("\nMethods:")
    for method_name in dir(my_instance):
        method = getattr(my_instance, method_name)
        if callable(method):
            print(f"{method_name}()")


'''
====================================UTILITY FUNCTIONS FOR WEBSOCKETS================================
'''


@database_sync_to_async
def asearch_object_by_attribute(server_class, **kwargs):
    return search_object_by_attribute(server_class, **kwargs)


'''
====================================BASIC FUNCTION UTILITY================================
'''


# return json string {'lobby_id': 'a', 'lobby_players': '7,', 'battle_init': False}
# => string list needs to be converted and booleans
def get_json_from_instance(instance):
    serialized_obj = serializers.serialize('json', [instance])
    test_json = json.loads(serialized_obj)
    return test_json[0]["fields"]


# same as before just for lists
def get_json_from_instances(instances):
    li = []
    for instance in instances:
        li.append(get_json_from_instance(instance))
    return json.dumps(li)


'''
check if the request method is a POST request.
As well as extracting a list of keys from the request. 
If a key is not available, a server message response is returned.
Otherwise a dictionary with the values is returned
'''


def basic_request_check(request, keys=None, ignore_missing_values=False) -> HttpResponse | dict[Any, Any | None]:
    if request.method != 'POST':
        return server_message_response(message="incorrect request method.")
    if keys is None:
        keys = []
    res = {}
    for key in keys:
        value = extract_request_value(request, key)
        if value is None:
            if ignore_missing_values:
                print(f"warning no {key} is given")
                continue
            else:
                return server_message_response(
                    message=f"no {key} is given")
        res[key] = value
    return res  # No missing values found


# generic get object according to input parameters in kwargs
def search_object_by_attribute(server_class, **kwargs):
    try:
        match server_class:
            case ServerClass.Player:

                return Player.objects.get(**kwargs)
            case ServerClass.Friendship:
                return Friendship.objects.get(**kwargs)
            case ServerClass.FriendRequest:
                return FriendRequest.objects.get(**kwargs)

            case ServerClass.Inventory:
                return Inventory.objects.get(**kwargs)
            case ServerClass.Lobby:
                return Lobby.objects.get(**kwargs)
            case ServerClass.TTTGame:

                return TTTGame.objects.get(**kwargs)
            case ServerClass.Guild:

                return Guild.objects.get(**kwargs)
            case ServerClass.ServerMessage:
                return ServerMessage.objects.get(**kwargs)
            case ServerClass.Leaderboard:

                return Leaderboard.objects.get(**kwargs)
            case ServerClass.Chat:
                return Chat.objects.get(**kwargs)
            case _:

                return None  # Handle unsupported server class

    except Exception as e:
        print(f"error {server_class, kwargs}\n", e)
        return None  # Handle exceptions such as ObjectDoesNotExist or others


# FOR OLDER VERSIONS THAN PYTHON 3.10
'''
if server_class == ServerClass.Player:
    return Player.objects.get(**kwargs)
elif server_class == ServerClass.Friendship:
    return Friendship.objects.get(**kwargs)
elif server_class == ServerClass.FriendRequest:
    return FriendRequest.objects.get(**kwargs)
elif server_class == ServerClass.Inventory:
    return Inventory.objects.get(**kwargs)
elif server_class == ServerClass.Lobby:
    return Lobby.objects.get(**kwargs)
elif server_class == ServerClass.TTTGame:
    return TTTGame.objects.get(**kwargs)
elif server_class == ServerClass.Guild:
    return Guild.objects.get(**kwargs)
elif server_class == ServerClass.ServerMessage:
    return ServerMessage.objects.get(**kwargs)
elif server_class == ServerClass.Leaderboard:
    return Leaderboard.objects.get(**kwargs)
else:
    return None  # Handle unsupported server class
'''


def check_values_in_request(request, keys):
    res = {}
    for key in keys:
        value = extract_request_value(request, key)
        if value is None:
            return server_message_response(
                message=f"no {key} is given")
        res[key] = value
    return res  # No missing values found


# in the lobby there are some fields which need to be changed so that unity can understands them
# e.g bools and the ids to names, in theory also floating point numbers according to the localization!
def get_readable_lobby_json(instance):
    result = convert_specific_fields(get_json_from_instance(instance))

    result["players"] = convert_ids_to_list_of_names(result["players"], ServerClass.Player)
    result = convert_specific_fields(result)
    return str(result)


'''
=========FRIENDLIST UTILITY FUNCTIONS=========
'''


# both methods could be combined and with extra boolean as input to get one or the other
def get_all_friendships_of_player(player_id):
    friend_requests = Friendship.objects.filter(Q(personOne__name=player_id) | Q(personTwo__name=player_id))
    return list(friend_requests)


def get_all_receives_of_player(player_id):
    friend_requests = FriendRequest.objects.filter(receiver__name=player_id)
    return list(friend_requests)


# TODO: try
'''

return FriendRequest.objects.get(
            (Q(requestor__name=player_name) & Q(receiver__name=friend_name)) | 
            (Q(requestor__name=friend_name) & Q(receiver__name=player_name))
        )
'''


def get_friend_request(player_name, friend_name):
    try:
        return FriendRequest.objects.get(
            (Q(requestor__name=player_name) & Q(receiver__name=friend_name)) |
            (Q(requestor__name=friend_name) & Q(receiver__name=player_name))
        )
    except Exception as e:
        print(f"Friend Request between {player_name} <-> {friend_name} ERROR:\n{e}")
        return None


# friendship between 2 person exists? yes or no
def is_friend(id_one, id_two):
    return True if get_friendship(id_one, id_two) is not None else False


def get_friendship(id_one, idTwo):
    for friendship in Friendship.objects.all():
        if friendship.personOne.name == id_one and friendship.personTwo.name == idTwo or friendship.personOne.name == idTwo and friendship.personTwo.name == id_one:
            return friendship
    return None


def friendrequest_to_readable(friendrequests):
    friend_requests_json = []
    for request in friendrequests:
        request_json = {
            "requestor": request.requestor.name,
            "receiver": request.receiver.name,
            "accepted": request.accepted
        }
        friend_requests_json.append(request_json)
    return json.dumps(friend_requests_json)


def friendship_to_readable(friendships):
    friend_ships_json = []
    for friendship in friendships:
        request_json = {
            "personOne": friendship.personOne.name,
            "personTwo": friendship.personTwo.name,
            "xp": friendship.xp
        }
        friend_ships_json.append(request_json)
    return json.dumps(friend_ships_json)


def convert_specific_fields(json_instance):
    for field in json_instance:
        if str(json_instance[field]) == "True":
            json_instance[field] = "true"
        if str(json_instance[field]) == "False":
            json_instance[field] = 'false'

        if str(json_instance[field]) == "None":
            json_instance[field] = 'null'

    return json_instance
