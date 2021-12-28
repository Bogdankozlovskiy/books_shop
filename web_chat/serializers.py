from rest_framework.serializers import ModelSerializer, DateTimeField
from web_chat.models import ChatMessage


class ChatMessageSerializer(ModelSerializer):
    date = DateTimeField(read_only=True, format="%d %B %Y y. %H:%M")

    class Meta:
        model = ChatMessage
        fields = ["text", "date"]
