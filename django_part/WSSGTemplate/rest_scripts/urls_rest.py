from django.urls import path

from WSSGTemplate.rest_scripts import views_basic, views_friendship, views_lobby, views_player, views_inventory, \
    views_guild, views_TTT, views_leaderboard,views_guild_functions

urlpatterns = [

    path("signin/", views_basic.signin),
    path("signout/", views_basic.signout),
    path("signup/", views_basic.signup),

    # every url to method for friendship stuff!
    # both urls are basically the same meaning so one could merge them
    path("add_friend/", views_friendship.add_friend),
    path("accept_friend_request/", views_friendship.add_friend),
    path("remove_friend/", views_friendship.remove_friend),
    # friendrequest stuff
    path("create_friend_request/", views_friendship.create_friend_request),
    path("get_friend_receives/", views_friendship.get_friend_receives),
    path("get_all_friendsships/", views_friendship.get_all_friendsships),

    path("remove_friend_request/", views_friendship.remove_friend_request),

    # every url to method for lobby stuff!
    path('get_lobby_by_id/', views_lobby.get_lobby_by_id),
    path('get_lobbies/', views_lobby.get_lobbies),
    path('set_lobby_by_id/', views_lobby.set_lobby_by_id),
    path('create_lobby/', views_lobby.create_lobby),
    path("join_lobby/", views_lobby.join_lobby),

    # every url to method for player stuff!
    path('get_player_by_id/', views_player.get_player_by_id),
    path('get_players/', views_player.get_players),
    path('set_player_by_id/', views_player.set_player_by_id),

    # every url to method for inventory stuff!
    path('get_inventory_by_id/', views_inventory.get_inventory_by_id),
    path('get_inventories/', views_inventory.get_inventories),
    path('set_inventory_by_id/', views_inventory.set_inventory_by_id),

    # every url to method for guild stuff!
    path('get_guild_by_id/', views_guild.get_guild_by_id),
    path('get_guilds/', views_guild.get_guilds),
    path('set_guild_by_id/', views_guild.set_guild_by_id),

    # urls for TTT example, basically extension of Lobby system
    path("update_game_action/", views_TTT.update_TTTGame),
    path("end_game/", views_TTT.end_game),
    path("get_game/", views_TTT.get_game),
    path("create_game/", views_TTT.create_TTTGame),
    path("surrender_game/", views_TTT.surrender_game),

    # urls for Leaderboard
    path("get_complete_leaderboard_by_category/", views_leaderboard.get_complete_leaderboard_by_category),
    path("update_score_of_player/", views_leaderboard.update_score_of_player),

    # urls for Guild
    path("join_guild/", views_guild_functions.join_guild),
    path("leave_guild/", views_guild_functions.leave_guild),
    path("debug_guild/", views_guild_functions.debug_guild),
]
