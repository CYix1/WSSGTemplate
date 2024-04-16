from channels.generic.websocket import AsyncWebsocketConsumer


# TODO: add an abstraction LAYER!
# ONE which handles the routing etc. like the rest part
# DEPRECATED

class BasicWSServer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("init")

    async def connect(self):
        await self.accept()
        print("connected: ")
        print(self.scope)

    async def disconnect(self, close_code):
        print("disconnected: " + str(close_code))

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data, bytes_data)
        await self.send("hi message received")
