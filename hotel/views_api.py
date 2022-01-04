from django.db.models.functions import ExtractDay
from rest_framework.filters import OrderingFilter
from hotel.models import OrderRoom
from hotel.serializers import OrderedRoomSerializer, OrderedRoomDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db.models import F
from hotel.utils import MyCustomFilter


class APIListOrderedRoom(ListAPIView):
    serializer_class = OrderedRoomSerializer
    queryset = OrderRoom.objects.annotate(duration__days=ExtractDay(F('end_date') - F('start_date')))\
        .annotate(total__price=F("price") * F("duration__days"))
    filter_backends = [OrderingFilter, MyCustomFilter]
    ordering_fields = ["id", "room", "price", "start_date", "end_date", "date", "duration__days", "total__price"]
    ordering = ['id']
    filtering_fields = {"duration__days__gte", "duration__days__lte", "total__price__gte", "total__price__lte"}


class APIRetrieveOrderedRoom(RetrieveAPIView):
    serializer_class = OrderedRoomDetailSerializer
    queryset = OrderRoom.objects.all()
