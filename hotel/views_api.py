from django.db.models.functions import ExtractDay
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
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
from django.views.decorators.http import condition, last_modified, etag
from django.views.decorators.vary import vary_on_headers, vary_on_cookie
from django.views.decorators.cache import cache_control, never_cache
from django.utils.cache import patch_response_headers
from django.utils.decorators import method_decorator
from datetime import datetime


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


def last_modify_func(request, **kwargs):
    return datetime(year=2022, month=1, day=10, hour=10, minute=20, second=10)


def current_etag(request, **kwargs):
    return "test_etag"


class APIListOrderedRoom(ListAPIView):
    serializer_class = OrderedRoomSerializer
    queryset = OrderRoom.objects.annotate(duration__days=ExtractDay(F('end_date') - F('start_date')))\
        .annotate(total__price=F("price") * F("duration__days"))
    filter_backends = [OrderingFilter, MyCustomFilter]
    ordering_fields = ["id", "room", "price", "start_date", "end_date", "date", "duration__days", "total__price"]
    ordering = ['id']
    filtering_fields = {"duration__days__gte", "duration__days__lte", "total__price__gte", "total__price__lte"}

    @method_decorator(condition(etag_func=current_etag, last_modified_func=last_modify_func), name="get")
    # @method_decorator(last_modified(last_modify_func), name="get")
    # @method_decorator(etag(current_etag), name="get")
    # @method_decorator(cache_control(max_age=40, public=True), name="get")
    # @method_decorator(never_cache)
    # @method_decorator(vary_on_headers("Cookie", "User-Agent"))
    # @method_decorator(vary_on_cookie)
    def get(self, request, * args, **kwargs):
        print(11111)
        return super(APIListOrderedRoom, self).get(request, *args, **kwargs)
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [SessionAuthentication]

    # def get_queryset(self):
    #     queryset = self.queryset.all()
    #     return get_objects_for_user(self.request.user, "hotel.view_orderroom", queryset, with_superuser=False)


class APIRetrieveOrderedRoom(RetrieveAPIView):
    serializer_class = OrderedRoomDetailSerializer
    queryset = OrderRoom.objects.all()
