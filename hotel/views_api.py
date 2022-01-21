import datetime
from hashlib import sha256
from django.db.models.functions import ExtractDay
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from hotel.models import OrderRoom
from hotel.serializers import OrderedRoomSerializer, OrderedRoomDetailSerializer, OrderedRoomCreateSerializr, \
    GuardianSerializer, ShowPermissionSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from django.db.models import F
from hotel.utils import MyCustomFilter
from guardian.shortcuts import assign_perm, get_objects_for_user
from django.contrib.auth.models import User, ContentType
from guardian.models.models import UserObjectPermission
from django.db.models import Q

from django.views.decorators.cache import cache_control
from django.views.decorators.http import etag, last_modified, condition
from django.utils.decorators import method_decorator


# HW: start check createing of Order Room, Can it be possible
# HW create new end point for removing permission


class DeletePermissionAPIView(RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ShowPermissionSerializer
    queryset = UserObjectPermission.objects.all()

    def list(self, request):
        orders = OrderRoom.objects.filter(user=request.user).values_list("id", flat=True)
        content_type = ContentType.objects.get(app_label="hotel", model="orderroom")
        permissions = UserObjectPermission.objects.filter(~Q(user=request.user) & Q(content_type=content_type, object_pk__in=list(orders)))
        serializer = self.serializer_class(permissions, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        orders = OrderRoom.objects.filter(user=self.request.user).values_list("id", flat=True)
        content_type = ContentType.objects.get(app_label="hotel", model="orderroom")
        permissions = self.queryset.filter(
            ~Q(user=self.request.user) &
            Q(content_type=content_type, object_pk__in=list(orders))
        )
        return permissions

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
        # do something or Not
        instance = serializer.save(user_id=self.request.user.id)
        assign_perm("hotel.view_orderroom", self.request.user, instance)


def my_function(request):
    date = OrderRoom.objects.all().order_by("date").last().date
    return datetime.datetime(year=date.year, month=date.month, day=date.day, hour=0, minute=0)


def my_little_fun(request):
    query_set = OrderRoom.objects.annotate(duration__days=ExtractDay(F('end_date') - F('start_date')))\
        .annotate(total__price=F("price") * F("duration__days"))
    setattr(request, "query_set", query_set)
    serializer = OrderedRoomSerializer(data=query_set, many=True)
    serializer.is_valid()
    return sha256(serializer.data.__str__().encode()).hexdigest()
    # return "my_key"


class APIListOrderedRoom(ListAPIView):
    serializer_class = OrderedRoomSerializer
    queryset = OrderRoom.objects.annotate(duration__days=ExtractDay(F('end_date') - F('start_date')))\
        .annotate(total__price=F("price") * F("duration__days"))
    filter_backends = [OrderingFilter, MyCustomFilter]
    ordering_fields = ["id", "room", "price", "start_date", "end_date", "date", "duration__days", "total__price"]
    ordering = ['id']
    filtering_fields = {"duration__days__gte", "duration__days__lte", "total__price__gte", "total__price__lte"}
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        if hasattr(self.request, "query_set"):
            queryset = self.request.query_set
        else:
            queryset = self.queryset.all()
        return get_objects_for_user(self.request.user, "hotel.view_orderroom", queryset, with_superuser=False)

    # @method_decorator(cache_control(max_age=40, private=True))
    # @method_decorator(last_modified(my_function))
    # @method_decorator(etag(my_little_fun))
    # @method_decorator(condition(etag_func=my_little_fun, last_modified_func=my_function))
    def get(self, *args, **kwargs):
        print("test query")
        return super().get(*args, **kwargs)


class APIRetrieveOrderedRoom(RetrieveAPIView):
    serializer_class = OrderedRoomDetailSerializer
    queryset = OrderRoom.objects.all()
