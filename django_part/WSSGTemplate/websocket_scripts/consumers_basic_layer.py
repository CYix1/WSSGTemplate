import json

from channels.generic.websocket import AsyncWebsocketConsumer

import utilities


class BasicWSServerLayer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.room_name = None
        self.room_group_name = None
        self.commands = {}

    async def connect(self):
        await self.accept()
        self.room_name = self.scope["url_route"]["kwargs"]["lobby_name"]
        self.room_group_name = f"group_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def check_command(self, text_data):
        # load data to get the single components (see ServerCommand.cs)
        js = json.loads(text_data)
        command = js["identifier"]
        extra_message = js["extraMessage"]
        message = js["message"]
        print(command, message)
        # Logic
        method = self.commands.get(command)
        if method is None:
            await self.send_message_to_client("error", "url path not known", "Server")
        else:
            await method(json.loads(message))

    async def send_message_to_client(self, message: str, identifier: str = "ERROR", extra_message: str = "server"):

        await self.send(
            utilities.server_message_json(extra_message=extra_message, identifier=identifier, message=message))

    async def receive(self, text_data=None, bytes_data=None):
        await self.check_command(text_data)

    async def send_broadcast_message(self, message: str, identifier: str = "ERROR", extra_message: str = "broadcast"):
        server_mes = utilities.server_message_json(
            extra_message=extra_message, message=message,
            identifier=identifier)
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message",
                                                                   "message": server_mes})

        # basic method for group_send other naming scheme doesn't tested!

    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket/clients
        await self.send(text_data=message)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
