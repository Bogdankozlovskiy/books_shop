from django.db.models.functions import ExtractDay
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from hotel.models import OrderRoom
from hotel.serializers import OrderedRoomSerializer, OrderedRoomDetailSerializer, OrderedRoomCreateSerializr, \
    GuardianSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.db.models import F
from hotel.utils import MyCustomFilter
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.contrib.auth.models import User
# HW: start check createing of Order Room, Can it be possible
# HW create new end point for removing permission


# class ShareGuardianPermission(GenericAPIView):
#     serializer_class = GuardianSerializer
#     converter = {"hotel.view_orderroom": 52, "hotel.change_orderroom": 50}
#
#     def post(self, request, valera):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data
#         data["content_type_id"] = 13
#         data["permission_id"] = self.converter[data.pop("permission")]
#         data['user_id'] = User.objects.filter(username=data.pop('user')).first().id
#         data['object_pk'] = valera
#         serializer.save()
#         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class ShareGuardianPermission(CreateAPIView):
    serializer_class = GuardianSerializer
    converter = {"hotel.view_orderroom": 52, "hotel.change_orderroom": 50}
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        data = serializer.validated_data
        data["content_type_id"] = 13
        data["permission_id"] = self.converter[data.pop("permission")]
        data['user_id'] = User.objects.filter(username=data.pop('user')).first().id
        serializer.save()


class APICreateOrderedRoom(CreateAPIView):
    serializer_class = OrderedRoomCreateSerializr
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def perform_create(self, serializer):
        instance = serializer.save(user_id=self.request.user.id)
        assign_perm("hotel.view_orderroom", self.request.user, instance)


class APIListOrderedRoom(ListAPIView):
    serializer_class = OrderedRoomSerializer
    queryset = OrderRoom.objects.annotate(duration__days=ExtractDay(F('end_date') - F('start_date')))\
        .annotate(total__price=F("price") * F("duration__days"))
    filter_backends = [OrderingFilter, MyCustomFilter]
    ordering_fields = ["id", "room", "price", "start_date", "end_date", "date", "duration__days", "total__price"]
    ordering = ['id']
    filtering_fields = {"duration__days__gte", "duration__days__lte", "total__price__gte", "total__price__lte"}
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        queryset = self.queryset.all()
        return get_objects_for_user(self.request.user, "hotel.view_orderroom", queryset, with_superuser=False)


class APIRetrieveOrderedRoom(RetrieveAPIView):
    serializer_class = OrderedRoomDetailSerializer
    queryset = OrderRoom.objects.all()
