from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from web_chat.serializers import ChatMessageSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "uniq_row",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "uniq_row",
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        if self.scope.get("user").is_authenticated:
            serializer = ChatMessageSerializer(data=content)
            serializer.is_valid(raise_exception=True)
            await sync_to_async(serializer.save)(user=self.scope.get("user"))
            await self.channel_layer.group_send(
                "uniq_row",
                {
                    'type': 'chat_message',
                    'message': serializer.data
                }
            )
        print("receive")

    async def chat_message(self, event):
        message = event['message']
        await self.send_json(
            content=message
        )
        print("chat_message")

    async def change_message(self, event):
        pass
