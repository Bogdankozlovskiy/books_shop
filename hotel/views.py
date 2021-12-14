from django.shortcuts import render
from hotel.models import Room, OrderRoom
from django.utils import timezone
from datetime import datetime
from django.db.models import Q, F


def search_room(request):
    if not request.GET:
        return render(request, "search_room.html")
    start_date = request.GET.get("start_date")
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    start_date = start_date.astimezone(timezone.get_current_timezone())
    end_date = request.GET.get("end_date")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    end_date = end_date.astimezone(timezone.get_current_timezone())

    free_rooms = Room.objects.filter(
        ~Q(ordered__in=OrderRoom.objects.filter(start_date__gt=start_date, end_date__lt=end_date))&
        ~Q(ordered__in=OrderRoom.objects.filter(start_date__gt=start_date, end_date__gt=end_date, start_date__lt=end_date))&
        ~Q(ordered__in=OrderRoom.objects.filter(start_date__lt=start_date, end_date__lt=end_date, end_date__gt=start_date))&
        ~Q(ordered__in=OrderRoom.objects.filter(start_date__lt=start_date, end_date__gt=end_date))
    ).annotate(price=F("price_for_day") * (end_date - start_date).days)
    return render(request, "show_rooms.html", {"free_rooms": free_rooms})
