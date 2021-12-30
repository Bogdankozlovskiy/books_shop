from django.urls import path
from web_chat import consumers


websocket_urlpatterns = [
    path('', consumers.ChatConsumer.as_asgi()),
]
