from rest_framework.serializers import ModelSerializer, IntegerField, FloatField
from hotel.models import OrderRoom


class OrderedRoomSerializer(ModelSerializer):
    duration_order = IntegerField(source="duration__days")
    total_price = FloatField(source="total__price")

    class Meta:
        model = OrderRoom
        fields = "__all__"
        extra_fields = ["duration_order", "total_price"]


class OrderedRoomDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderRoom
        fields = "__all__"
        depth = 1
