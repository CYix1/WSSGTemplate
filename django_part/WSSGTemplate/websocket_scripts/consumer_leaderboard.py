import utilities
from ServerClass import ServerClass
from WSSGTemplate.models import Leaderboard
from WSSGTemplate.websocket_scripts.consumers_basic_layer import BasicWSServerLayer


class WSLeaderboard(BasicWSServerLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.commands = {
            "UPDATE ENTRY": self.handle_update,
        }

    async def handle_update(self, data):
        player_req = data["id"]
        category_req = data["category"]
        score_req = data["score"]

        (leaderboard, entry) = await self.get_entry_of_player_in_category(player_req, category_req)

        if leaderboard is None:
            leaderboard = Leaderboard(category=category_req)
            leaderboard.save()

        if entry is None:
            # Create a new entry if the player does not exist in the leaderboard's entries list
            new_entry = {"player": player_req, "score": score_req}
            leaderboard.entries.append(new_entry)
        else:
            entry["score"] = score_req

        leaderboard.save()

        order = "desc"  # default value

        # If "order" is provided, sort the entries accordingly
        if "order" in data.keys():
            order = data["order"]

        if order.lower() == "asc":
            sorted_entries = sorted(leaderboard.entries, key=lambda x: x["score"])
        elif order.lower() == "desc":
            sorted_entries = sorted(leaderboard.entries, key=lambda x: x["score"], reverse=True)
        else:
            await  self.send_message_to_client("invalid order value")
            return
        leaderboard.entries = sorted_entries
        await self.send_broadcast_message(message=str(utilities.get_json_from_instance(leaderboard)),
                                          identifier="DATA", extra_message="leader_board_data")

    async def get_entry_of_player_in_category(self, player_name, category):
        leaderboard = await utilities.asearch_object_by_attribute(ServerClass.Leaderboard, category=category)
        if leaderboard is None:
            return None, None
        for entry in leaderboard.entries:
            if entry["player"] == player_name:
                return leaderboard, entry

        return leaderboard, None
