from django.http import HttpResponse

import utilities
from ServerClass import ServerClass
from WSSGTemplate.models import Leaderboard

'''
get_complete_leaderboard_by_category receives: "category" optional: "order"
returns a leaderboard given an optional order. default is descending order!
'''


def get_complete_leaderboard_by_category(request):
    result_from_check = utilities.basic_request_check(request, ["category", "order"], True)
    if isinstance(result_from_check, HttpResponse):
        return result_from_check

    category_req = result_from_check["category"]
    # Attempt to get the leaderboard by category
    leaderboard = utilities.search_object_by_attribute(ServerClass.Leaderboard, category=category_req)
    # If the leaderboard does not exist, create a new one
    if leaderboard is None:
        leaderboard = Leaderboard(category=category_req)
        leaderboard.save()
        return utilities.server_message_response(message="created leaderboard", identifier="MESSAGE", status=200)

    order = "desc"  # default value

    # If "order" is provided, sort the entries accordingly
    if "order" in result_from_check.keys():
        order = result_from_check["order"]

    if order.lower() == "asc":
        sorted_entries = sorted(leaderboard.entries, key=lambda x: x["score"])
    elif order.lower() == "desc":
        sorted_entries = sorted(leaderboard.entries, key=lambda x: x["score"], reverse=True)
    else:
        return utilities.server_message_response("invalid order value")

    leaderboard.entries = sorted_entries

    return utilities.server_message_response(message=str(utilities.get_json_from_instance(leaderboard)),
                                             identifier="DATA", status=200)


'''
update_score_of_player receives: "id", "category", "score" 
updates the score of a player in a leaderboard category.
It is a little workaround since the entries are not modeled but just saved as a Json "string"
If the entry is non existent, it get's created!
'''


def update_score_of_player(request):
    result_from_check = utilities.basic_request_check(request, ["id", "category", "score"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check
    player_req = result_from_check["id"]
    category_req = result_from_check["category"]
    score_req = result_from_check["score"]

    (leaderboard, entry) = get_entry_of_player_in_category(player_req, category_req)

    if leaderboard is None:
        return utilities.server_message_response(message="category for leaderboard does not exists")

    if entry is None:
        # Create a new entry if the player does not exist in the leaderboard's entries list
        new_entry = {"player": player_req, "score": score_req}
        leaderboard.entries.append(new_entry)
    else:
        entry["score"] = score_req

    leaderboard.save()
    return utilities.server_message_response(message="updated entry", identifier="NOTHING", status=200)


'''
get_entry_of_player_in_category receives: "player_namer", "category"
returns either 
None -> no leaderboard at all
leaderboard, entry -> intended return values
leaderboard, None -> leadeboard exists but no entry
'''


def get_entry_of_player_in_category(player_name, category):
    leaderboard = utilities.search_object_by_attribute(ServerClass.Leaderboard, category=category)
    if leaderboard is None:
        return None, None
    for entry in leaderboard.entries:
        if entry["player"] == player_name:
            return leaderboard, entry

    return leaderboard, None
