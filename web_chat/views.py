from django.shortcuts import render, redirect
from web_chat.models import ChatMessage
from web_chat.serializers import ChatMessageSerializer


def index(request):
    messages = ChatMessage.objects.all().select_related("user").only("date", "text", "user__username")
    return render(request, "chat_index.html", {"messages": messages})


def add_new_message(request):
    serializer = ChatMessageSerializer(data=request.POST)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return redirect("Chat:index")
