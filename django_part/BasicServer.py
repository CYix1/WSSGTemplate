import asyncio

from websockets.server import serve

# DEPRECATED

dic = {}


async def echo(websocket):
    async for message in websocket:
        if "clientConnect" in message:

            getUID = message.split("|")[1]

            dic[getUID] = 0

            await websocket.send("YES Server")
        else:

            dic[message] += 1
            print(f"from client ({int(message)})   Total: {len(dic)} full: {dic}")
            await websocket.send(message)


async def main():
    async with serve(echo, "localhost", 8000, close_timeout=None):
        await asyncio.Future()  # run forever


asyncio.run(main())
