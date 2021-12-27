import asyncio
from websockets import connect


async def hello(uri):
    websocket = await connect(uri)
    await websocket.send("Hello world!")
    return await websocket.recv()

asyncio.run(hello("ws://localhost:5555"))
