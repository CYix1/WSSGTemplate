from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import *

import utilities
from ServerClass import ServerClass
from WSSGTemplate.models import Player, Inventory

'''
signup receives: "username", "password1", "password2"
and creates/authenticates/logins this user as well as their inventory
'''


def signup(request):
    result_from_check = utilities.basic_request_check(request, ["username", "password1", "password2"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check

    # Checks if the correct data/keys are being send to correctly extract them.
    # Checks if some the value according to the keys exists (are in the database)
    username_req = result_from_check["username"]

    password1_req = result_from_check["password1"]
    password2_req = result_from_check["password2"]

    player = utilities.search_object_by_attribute(ServerClass.Player, name=username_req)
    if player:
        return utilities.server_message_response(f"user already exists")

    if password1_req != password2_req:
        return utilities.server_message_response(f"password check was wrong")

    # Instead of checking for the form data ourselves, we use the already
    # existing UserCreationForm.
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return utilities.server_message_response(f'invalid form: {form}')

    # This creates a user from that form
    form.save()

    # We don't have to check if the username and password are correct
    # because we just created that exact user.
    user = authenticate(username=username_req, password=password1_req)
    login(request, user)

    player = Player(user=user, name=username_req)

    # Don't forget to save at the end of all the changes to table contents
    player.save()

    # every player has an inventory which is created during signup
    player_inventory = Inventory(owner=player)
    player_inventory.save()

    return utilities.server_message_response(identifier="MESSAGE", message='successful signup', status=200)


# signout function from template
# called signout to prevent name duplication with the logout function of django
def signout(request):
    logout(request)
    return utilities.server_message_response(identifier="MESSAGE", message='successful logout', status=200)


'''
signin receives: "username","password"
and logins this user
'''


def signin(request):
    result_from_check = utilities.basic_request_check(request, ["username", "password"])
    if isinstance(result_from_check, HttpResponse):
        return result_from_check

    username_req = result_from_check["username"]
    password_req = result_from_check["password"]

    player = utilities.search_object_by_attribute(ServerClass.Player, name=username_req)
    if player is None:
        return utilities.server_message_response(
            message=f" user does not exist")

    if player.user.is_authenticated:
        return utilities.server_message_response(status=200, identifier="NOTHING",
                                                 message=f'{username_req} already signed in')

    # authenticate() only returns a user if username and password are correct
    user = authenticate(request, username=username_req, password=password_req)

    if user is None:
        return utilities.server_message_response(
            message=f'username or password is wrong ')
    login(request, user)

    return utilities.server_message_response(status=200, identifier="MESSAGE", message='successful signin')
