from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, IntegerField, FloatField, ChoiceField, CharField, SerializerMethodField
from guardian.models import UserObjectPermission
from hotel.models import OrderRoom


class ShowPermissionSerializer(ModelSerializer):
    user_name = CharField(source="user.username")
    permission_name = CharField(source="permission.name")
    object_body = SerializerMethodField()

    class Meta:
        model = UserObjectPermission
        fields = ["id", "user_name", "object_body", "permission_name"]

    def get_object_body(self, permission):
        order_room = permission.content_type.model_class().objects.get(pk=permission.object_pk)
        return str(order_room)


class GuardianSerializer(ModelSerializer):
    permission = CharField()
    user = CharField()

    class Meta:
        model = UserObjectPermission
        fields = ["permission", "object_pk", "user"]

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
        fields = ["id", 'room', "start_date", "end_date"]
