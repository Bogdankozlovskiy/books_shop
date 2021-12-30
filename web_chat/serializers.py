from rest_framework.serializers import ModelSerializer, DateTimeField, CharField
from web_chat.models import ChatMessage


class ChatMessageSerializer(ModelSerializer):
    date = DateTimeField(read_only=True, format="%d %B %Y y. %H:%M")
    user = CharField(read_only=True, source="user.username")

    class Meta:
        model = ChatMessage
        fields = ["text", "date", "user"]
