from django.urls import re_path

from WSSGTemplate.Core.Websocket import consumers_basic_layer, consumers_basic
from WSSGTemplate.Examples.Chat import consumer_chat
from WSSGTemplate.Examples.Guild import consumer_guild_function
from WSSGTemplate.Examples.Leaderboard.Websocket import consumer_leaderboard
from WSSGTemplate.Examples.Lobby.Websocket import consumer_example_lobby
from WSSGTemplate.Examples.TicTacToe.Websocket import consumer_example_game

# the websocket urls.

websocket_urlpatterns = [
    re_path(r'ws/basic/$', consumers_basic.BasicWSServer.as_asgi()),
    re_path(r'ws/layer/(?P<lobby_name>\w+)/$', consumers_basic_layer.BasicWSServerLayer.as_asgi()),

    re_path(r'ws/TTT/(?P<lobby_name>\w+)/$', consumer_example_lobby.TTTWSLobby.as_asgi()),
    re_path(r'ws/TTTGame/(?P<lobby_name>\w+)/$', consumer_example_game.TTTWSGame.as_asgi()),
    re_path(r'ws/WSLeaderboard/(?P<lobby_name>\w+)/$', consumer_leaderboard.WSLeaderboard.as_asgi()),
    re_path(r'ws/ChatWS/(?P<lobby_name>\w+)/$', consumer_chat.WSChat.as_asgi()),

    re_path(r'ws/GuildWS/(?P<lobby_name>\w+)/$', consumer_guild_function.WSGuildfunction.as_asgi()),
]
'''
(?P<XXXX>\w+)
corresponds to   self.scope["url_route"]["kwargs"]["XXXX"] in the connect method.
double check with django_part/django_part/asgi.py show_print=True
'''
