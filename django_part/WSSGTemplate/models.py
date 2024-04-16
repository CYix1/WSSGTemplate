import json

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class TestPos(models.Model):
    uid = models.IntegerField(default=-1, primary_key=True)
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    z = models.FloatField(default=0.0)

    def __str__(self):
        return f"UIsD: {self.uid}, Position: ({self.x}, {self.y}, {self.z})"


class Player(models.Model):
    genericID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, default="", unique=True)
    playerClass = models.CharField(max_length=1000, default="")
    guild = models.ForeignKey('Guild', on_delete=models.SET_NULL, null=True, blank=True, related_name='guild_members')

    def __str__(self):
        return f"{self.genericID}|{self.user}|{self.name}|{self.playerClass}"


# Bidirectional Friendship
class Friendship(models.Model):
    genericID = models.AutoField(primary_key=True)
    personOne = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='friendships_as_person_one', null=True,
                                  default=None)
    personTwo = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='friendships_as_person_two', null=True,
                                  default=None)
    xp = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.personOne} <-> {self.personTwo}| {self.xp}"


# Bidirectional Friendship, which can be accepted
class FriendRequest(models.Model):
    genericID = models.AutoField(primary_key=True)
    requestor = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_friend_requests', null=True,
                                  default=None)
    receiver = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='received_friend_requests', null=True,
                                 default=None)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.requestor} -> {self.receiver}| {self.genericID}"


# plain Inventory string
class Inventory(models.Model):
    genericID = models.AutoField(primary_key=True)
    owner = models.OneToOneField(Player, on_delete=models.CASCADE, null=True, default=None)
    inventory = models.JSONField(default=list)

    def __str__(self):
        return f"{self.owner.name} -> {self.inventory}"


# lobby
class Lobby(models.Model):
    genericID = models.AutoField(primary_key=True)
    lobbyID = models.CharField(max_length=50, default="1")
    players = models.ManyToManyField(Player)
    finishSelecting = models.JSONField(default=list)
    isActive = models.BooleanField(default=True)
    startGame = models.BooleanField(default=False)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True,
                               default=None, related_name='lobby_winner')

    def __str__(self):
        return f"Lobby {self.lobbyID} {'(Active)' if self.isActive else '(Inactive)'}"


class TTTGame(models.Model):
    genericID = models.AutoField(primary_key=True)
    host = models.ForeignKey(Player, null=True, on_delete=models.CASCADE,
                             default=None, related_name='game_host')
    opponent = models.ForeignKey(Player, null=True, on_delete=models.CASCADE,
                                 default=None, related_name='game_opponent')
    lobby = models.ForeignKey(Lobby, null=True, on_delete=models.CASCADE, default=None)
    action = models.JSONField(default=["", "", "", "", "", "", "", "", ""])
    current_index = models.IntegerField(default=0)

    def __str__(self):
        return f"TTTGAME {self.lobby.lobbyID}"


class Guild(models.Model):
    genericID = models.AutoField(primary_key=True)
    guildPlayers = models.ManyToManyField(Player, related_name='guilds')
    guildOwner = models.OneToOneField(Player, on_delete=models.CASCADE, related_name='owned_guild_backref')
    guildName = models.CharField(max_length=1000, default="guild")


class ServerMessage(models.Model):
    genericID = models.AutoField(primary_key=True)
    extraMessage = models.CharField(max_length=1000, default="test")
    message = models.JSONField(default=list)  # json
    identifier = models.CharField(max_length=1000, default="test")

    def __str__(self):
        return json.dumps({
            "extraMessage": self.extraMessage,
            "message": self.message,
            "identifier": self.identifier
        })


class Leaderboard(models.Model):
    genericID = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100, unique=True)
    entries = models.JSONField(default=list)

    '''
    entries: [{"player": "test", "score": 42},{"player": "Max Mustermann", "score": 69}]
    '''

    def __str__(self):
        return str(json.dumps({
            "category": self.category,
            "entries": self.entries,
        }))


class Chat(models.Model):
    genericID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    messages = models.JSONField(default=list)
    '''
    messages: [{"username": "test", "time": 42, "message": "test"}, {"username": "test", "time": 42, "message": "test"}]
    '''

    def __str__(self):
        return json.dumps({

            "name": self.name,
            "messages": str(self.messages)[0:100] + "...",
        })
