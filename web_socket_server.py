import websockets
import asyncio
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError


all_client = []


async def send_message(message):
    for client in all_client:
        try:
            await client.send(message)
        except ConnectionClosedOK:
            all_client.remove(client)


async def accept_new_client(client_socket, path):
    print("new client connected")
    all_client.append(client_socket)
    while True:
        try:
            new_message = await client_socket.recv()
        except ConnectionClosedOK:
            await send_message("one client live us")
            break
        except ConnectionClosedError:
            print("we lost connection")
            break
        else:
            print("client send:", new_message)
            await send_message(new_message)


async def start_server():
    print("starting server")
    await websockets.serve(accept_new_client, "localhost", 5555)


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(start_server())
event_loop.run_forever()
