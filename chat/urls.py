from chat import views
from django.urls import path


app_name = "Chat"
# https://channels.readthedocs.io/en/stable/introduction.html
urlpatterns = [
    path("", views.index, name="chat"),
    path("room_redirect/", views.room_redirect, name="room-redirect"),
    path("<str:room_name>/", views.room, name="room"),
]
