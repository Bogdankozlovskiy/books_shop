from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, IntegerField, FloatField, ChoiceField, CharField
from guardian.models import UserObjectPermission
from hotel.models import OrderRoom


class GuardianSerializer(ModelSerializer):
    permission = ChoiceField(
        choices=[("hotel.view_orderroom", "hotel.view_orderroom"),
                 ("hotel.change_orderroom", "hotel.change_orderroom")]
    )
    user = CharField()

    class Meta:
        model = UserObjectPermission
        fields = ["permission", "object_pk", "user"]
        
    def to_representation(self, instance):
        result = super().to_representation(instance)
        result['permission'] = result['permission'].codename
        return result

    def validate(self, attrs):
        ordered_room = OrderRoom.objects.get(pk=self.context['request'].data['object_pk'])
        if ordered_room.user != self.context['request'].user:
            raise ValidationError({
                "permission": "Only Owner can Share Permission"
            }, code='invalid')
        return attrs


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


class OrderedRoomCreateSerializr(ModelSerializer):
    class Meta:
        model = OrderRoom
        fields = ['room', "start_date", "end_date"]
