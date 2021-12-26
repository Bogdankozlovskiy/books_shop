from chat import views
from django.urls import path


app_name = "Chat"
urlpatterns = [
    path("", views.index, name="chat"),
    path("<str:room_name>/", views.room, name="room"),
]
