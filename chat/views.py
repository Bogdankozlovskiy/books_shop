from django.shortcuts import render, redirect


def index(request):
    return render(request, "chat.html")


def room(request, room_name=None):
    return render(request, "room.html", {"room_name": room_name})


def room_redirect(request):
    return redirect("Chat:room", room_name=request.GET.get("room_name"))
