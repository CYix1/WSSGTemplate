import json

from websockets.sync.client import connect

# DEPRECATED
url = "ws://127.0.0.1:8000/ws/layer/test/"


def single_request():
    with connect(url) as websocket:
        websocket.send(json.dumps({"type": "chat.message", "message": "BASICCLIENTO"}))
        message = websocket.recv()
        print(f"Received: {message} ")


def listening():
    with connect(url) as websocket:
        while True:
            message = websocket.recv()
            print(f"Received: {message}")


single_request()
listening()
