from django.contrib import admin
from hotel.models import Room, OrderRoom
from guardian.admin import GuardedModelAdmin


class OrderRoomInline(admin.StackedInline):
    model = OrderRoom
    readonly_fields = ['price']


class RoomAdmin(admin.ModelAdmin):
    inlines = [OrderRoomInline]


class GuardianOrderRoom(GuardedModelAdmin):
    pass


admin.site.register(Room, RoomAdmin)
admin.site.register(OrderRoom, GuardianOrderRoom)
