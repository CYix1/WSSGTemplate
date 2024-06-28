from django.urls import re_path

from WSSGTemplate.websocket_scripts import consumers_basic, consumers_basic_layer, \
    consumer_example_lobby, consumer_example_game, consumer_chat, consumer_leaderboard, consumer_guild_function

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
