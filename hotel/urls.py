from django.urls import path
from hotel.views import search_room, my_account
from hotel.views_api import APIListOrderedRoom, APIRetrieveOrderedRoom, APICreateOrderedRoom, ShareGuardianPermission,\
DeletePermissionAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("api_v1/permissions", DeletePermissionAPIView)

app_name = 'Hotel'
urlpatterns = [
    path("serach_room/", search_room, name="search-room"),
    path("serach_room/<int:room_id>/", search_room, name="order-room"),
    path("my_account/", my_account, name="my-account"),
    path("api_v1/list_ordered_room/", APIListOrderedRoom.as_view(), name="list-ordered-room"),
    path("api_v1/list_ordered_room/<int:pk>/", APIRetrieveOrderedRoom.as_view(), name="retrieve-ordered-room"),
    path("api_v1/create_order_room/", APICreateOrderedRoom.as_view(), name="create-order-room"),
    path("api_v1/share_order/", ShareGuardianPermission.as_view(), name="share-order-room"),
    # path("api_v1/permissions/", DeletePermissionAPIView.as_view({"get": "list"}), name="show-permissions"),
    path("api_v1/permissions/<int:pk>/", DeletePermissionAPIView.as_view({"delete": "destroy"}), name="delete-permissions")
] + router.urls
