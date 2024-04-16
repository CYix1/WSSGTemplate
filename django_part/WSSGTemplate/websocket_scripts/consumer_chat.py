import utilities
from ServerClass import ServerClass
from WSSGTemplate.models import Chat
from WSSGTemplate.websocket_scripts.consumers_basic_layer import BasicWSServerLayer


class WSChat(BasicWSServerLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("init")
        self.commands = {
            "UPDATE ENTRY": self.handle_update,
        }

    async def handle_update(self, data):
        print(data)

        name_req = data["name"]

        chat = await utilities.asearch_object_by_attribute(ServerClass.Chat, name=name_req)
        if chat is None:
            chat = Chat(name=name_req)
            chat.save()
            await self.send_message_to_client(f"CHAT WITH NAME {name_req} CREATED")

        # update only if available to basically remove the need for another method
        if "message" in data:
            chat.messages.append(data["message"])
            chat.save()

        sorted_entries = sorted(chat.messages, key=lambda x: x["time"])
        chat.messages = sorted_entries

        await self.send_broadcast_message(message=str(utilities.get_json_from_instance(chat)),
                                          identifier="DATA", extra_message="chat_data")
