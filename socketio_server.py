from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def chat_message(sid, data):
    print("message ", data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


web.run_app(app, host="localhost", port=5555)
