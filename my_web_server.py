import asyncio
import websockets
from aiohttp import ClientSession

all_clients = []


async def safe_message(message):
    client = ClientSession()
    response = await client.post(
        "http://localhost:8000/api_v1/create_message/",
        data={"text": message}
    )
    await client.close()
    return await response.text()


async def echo(websocket):
    print("accept new client")
    all_clients.append(websocket)
    while True:
        message = await websocket.recv()
        message = await safe_message(message)
        print(message)
        for client in all_clients:
            if not client.closed:
                await client.send(message)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
