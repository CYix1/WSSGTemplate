from django.http import HttpResponse

import utilities
from ServerClass import ServerClass
from ..models import Friendship, FriendRequest

'''
add_friend receives: "id", "friendID"
and adds a relationship between user(id) and user(friendID)
'''


def add_friend(request):
    result_from_check = utilities.basic_request_check(request, ["id", "friendID"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check

    player_name = result_from_check["id"]
    friend_name = result_from_check["friendID"]

    player = utilities.search_object_by_attribute(ServerClass.Player, name=player_name)
    # Basic check if available
    if player is None:
        return utilities.server_message_response(
            message=f"player {player_name} was not found")

    friend = utilities.search_object_by_attribute(ServerClass.Player, name=friend_name)
    if friend is None:
        return utilities.server_message_response(
            message=f"player {friend_name} was not found")

    # check for friend request
    req = utilities.get_friend_request(player_name=player.name, friend_name=friend.name)
    if req is None:
        return utilities.server_message_response(
            message=f"no friend request between {player.name} and {friend.name} was found")

    # save friendship
    friendship = Friendship(personOne=player, personTwo=friend,
                            xp=0)
    friendship.save()
    req.delete()

    return utilities.server_message_response(status=200, identifier="MESSAGE",
                                             message=f"Friendship between {player.name} and {friend.name} was established")


'''
create_friend_request receives: "id", "friendID"
and creates a friendrequest from the requestor(id) to the receiver(friendID)
'''


def create_friend_request(request):
    result_from_check = utilities.basic_request_check(request, ["id", "friendID"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    player_name_req = result_from_check["id"]
    friend_name_req = result_from_check["friendID"]

    # get both players
    player_requestor = utilities.search_object_by_attribute(ServerClass.Player, name=player_name_req)
    if player_requestor is None:
        return utilities.server_message_response(
            message=f"no player was found")
    friend_receiver = utilities.search_object_by_attribute(ServerClass.Player, name=friend_name_req)
    if friend_receiver is None:
        return utilities.server_message_response(
            message=f"no friend was found")
    if player_name_req == friend_name_req:
        return utilities.server_message_response(
            message=f"don't add yourself")

    # get friend request
    friend_request = utilities.get_friend_request(player_name=player_name_req,
                                                  friend_name=friend_name_req)
    if friend_request is not None:
        return utilities.server_message_response(
            message=f"this request is already available")

    if utilities.is_friend(player_name_req, friend_name_req):
        return utilities.server_message_response(
            message=f"You're already friends, no request is needed")
    # create a new request and save it
    friend_request = FriendRequest(requestor=player_requestor, receiver=friend_receiver)
    friend_request.save()

    return utilities.server_message_response(status=200, identifier="MESSAGE",
                                             message=f"Request was created and sent!")


'''
get_friend_receives receives: "id"
and returns a list with all RECEIVED friend requests  for user(id)
'''


def get_friend_receives(request):
    result_from_check = utilities.basic_request_check(request, ["id"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    player_name_req = result_from_check["id"]

    friend_requests = utilities.get_all_receives_of_player(player_name_req)
    if len(friend_requests) == 0:
        return utilities.server_message_response(
            message=f"No FriendshipRequest with {player_name_req}")

    readable_friend_requests = utilities.friendrequest_to_readable(friend_requests)

    return utilities.server_message_response(status=200, identifier="DATA", message=readable_friend_requests)


'''
remove_friend receives: "id", "friendID"
and removes the friend relationship between user(id) and friend(id)
'''


def remove_friend(request):
    result_from_check = utilities.basic_request_check(request, ["id", "friendID"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    player_name_req = result_from_check["id"]
    friend_name_req = result_from_check["friendID"]

    friendship = utilities.get_friendship(player_name_req, friend_name_req)

    if friendship is None:
        return utilities.server_message_response(
            message=f"no friendship between {player_name_req} <-> {friend_name_req} was found")
    friendship.delete()
    return utilities.server_message_response(status=200, identifier="NOTHING",
                                             message=f"you removed {friend_name_req} from your friends")


'''
get_all_friendsships receives: "id"
and returns a list of all friendships the user(id) is in. Depending on the request made beforehand, the user(id) can be
either personOne or personTwo see Friendship in models.py . It is being taken care of in utilities.get_all_friendships_of_player
'''


def get_all_friendsships(request):
    result_from_check = utilities.basic_request_check(request, ["id"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    player_name_req = result_from_check["id"]
    friendships = utilities.get_all_friendships_of_player(player_name_req)

    if len(friendships) == 0:
        return utilities.server_message_response(
            message=f"No Friendship with {player_name_req}")

    readable_friendships = utilities.friendship_to_readable(friendships)
    return utilities.server_message_response(status=200, identifier="DATA", message=readable_friendships)


'''
remove_friend_request receives: "id", "friendID"
and removes the reqeust, e.g the request got declined
'''


def remove_friend_request(request):
    result_from_check = utilities.basic_request_check(request, ["id", "friendID"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    player_name_req = result_from_check["id"]
    friend_name_req = result_from_check["friendID"]

    friendrequest = utilities.get_friend_request(player_name_req, friend_name_req)
    if friendrequest is None:
        return utilities.server_message_response(
            message=f"no friendrequest from {player_name_req} to {friend_name_req}")

    friendrequest.delete()
    return utilities.server_message_response(status=200, identifier="NOTHING",
                                             message=f"friendrequest from {friend_name_req} was successfully declined")
