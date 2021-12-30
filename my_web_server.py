import asyncio
import websockets
from aiohttp import ClientSession
from http.cookies import SimpleCookie


all_clients = []


async def safe_message(message, websocket):
    cookie = SimpleCookie(websocket.request_headers.get("Cookie"))
    csrf_token = cookie.get("csrftoken")
    session_id = cookie.get("sessionid")
    if csrf_token is not None and session_id is not None:
        client = ClientSession()
        response = await client.post(
            "http://localhost:8000/api_v1/create_message/",
            data={"text": message, "csrfmiddlewaretoken": csrf_token.value},
            cookies={"sessionid": session_id.value, "csrftoken": csrf_token.value}
        )
        await client.close()
        return await response.text()
    return None


async def echo(websocket):
    print("accept new client")
    all_clients.append(websocket)
    while True:
        message = await websocket.recv()
        message = await safe_message(message, websocket)
        if message is None:
            continue
        print(message)
        for client in all_clients:
            if not client.closed:
                await client.send(message)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
