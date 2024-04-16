from enum import Enum


# enum for some methods in utilites.py etc.
class ServerClass(Enum):
    Player = 0
    Friendship = 1
    FriendRequest = 2
    Inventory = 3
    Lobby = 4
    TTTGame = 5
    Guild = 6
    ServerMessage = 7
    Leaderboard = 8
    Chat = 9
