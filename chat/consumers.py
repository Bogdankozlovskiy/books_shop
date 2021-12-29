from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.sites.models import Site


class ChatConsumer(AsyncJsonWebsocketConsumer):
    room_name = None
    room_group_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        if self.scope['user'].is_authenticated:
            await self.receive_json({"message": f"say hello to {self.scope['user'].username}"})
        else:
            await self.receive_json({"message": f"say hello to Anonymous"})

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        if self.scope['user'].is_authenticated:
            await self.receive_json({"message": f"say good buy to {self.scope['user'].username}"})
        else:
            await self.receive_json({"message": f"say good buy to Anonymous"})

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        # Send message to room group
        site_name = (await database_sync_to_async(Site.objects.get_current)()).name
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content['message'] + site_name
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send_json(content={'message': event['message']})
