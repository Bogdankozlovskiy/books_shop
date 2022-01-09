from django.http import HttpResponse
from django.shortcuts import render, redirect
from hotel.models import Room, OrderRoom
from django.db.models import Q, F
from hotel.utils import convert_str_date_to_timezone_date
from django.contrib import messages


def search_room(request, room_id=None):
    """
    @param request: blabla
    @param room_id: bal bla
    @return: bla
    """
    if not request.GET and request.method == "GET":
        storage = messages.get_messages(request)
        msgs = [(msg.message, msg.tags, msg.extra_tags) for msg in storage]
        print(msgs)
        print(storage.used)
        messages.warning(request, "hello world", "extra hello")
        messages.add_message(request, messages.ERROR, "Error hello", "extra error")
        return render(request, "search_room.html")
    if request.method == "POST":
        start_date = convert_str_date_to_timezone_date(request.POST.get("start_date"))
        end_date = convert_str_date_to_timezone_date(request.POST.get("end_date"))
        OrderRoom.objects.create(
            room_id=room_id,
            user_id=request.user.id,
            start_date=start_date,
            end_date=end_date
        )
        return redirect("Hotel:my-account")

    start_date = convert_str_date_to_timezone_date(request.GET.get("start_date"))
    end_date = convert_str_date_to_timezone_date(request.GET.get("end_date"))

    free_rooms = Room.objects.filter(
        ~Q(ordered__in=OrderRoom.objects.filter(start_date__gt=start_date, end_date__lt=end_date))&
        ~Q(ordered__in=OrderRoom.objects.filter(start_date__gt=start_date, end_date__gt=end_date, start_date__lt=end_date))&
        ~Q(ordered__in=OrderRoom.objects.filter(start_date__lt=start_date, end_date__lt=end_date, end_date__gt=start_date))&
        ~Q(ordered__in=OrderRoom.objects.filter(start_date__lt=start_date, end_date__gt=end_date))
    ).annotate(price=F("price_for_day") * (end_date - start_date).days)
    return render(request, "show_rooms.html", {"free_rooms": free_rooms, "start_date": start_date, "end_date": end_date})


def my_account(request):
    return HttpResponse("hello world")
