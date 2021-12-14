from django.urls import path
from hotel.views import search_room, my_account

app_name = 'Hotel'
urlpatterns = [
    path("serach_room/", search_room, name="search-room"),
    path("serach_room/<int:room_id>/", search_room, name="order-room"),
    path("my_account/", my_account, name="my-account")
]
