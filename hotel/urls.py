from django.urls import path
from hotel.views import search_room, my_account
from hotel.views_api import APIListOrderedRoom, APIRetrieveOrderedRoom


app_name = 'Hotel'
urlpatterns = [
    path("serach_room/", search_room, name="search-room"),
    path("serach_room/<int:room_id>/", search_room, name="order-room"),
    path("my_account/", my_account, name="my-account"),
    path("api_v1/list_ordered_room/", APIListOrderedRoom.as_view(), name="list-ordered-room"),
    path("api_v1/list_ordered_room/<int:pk>/", APIRetrieveOrderedRoom.as_view(), name="retrieve-ordered-room"),
]
