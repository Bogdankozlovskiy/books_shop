from django.shortcuts import render


def index(request):
    if room_name := request.GET.get("room_name"):
        return render(request, "room.html", {"room_name": room_name})
    return render(request, "chat.html")
