from django.urls import path
from chat import consumers


websocket_urlpatterns = [
    path(r'ws/chat/<room_name>/', consumers.ChatConsumer.as_asgi()),
]
