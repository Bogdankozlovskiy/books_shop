from django.urls import path
from web_chat import views

app_name = "Chat"

urlpatterns = [
    path("", views.index, name="index"),
    path("new_message/", views.add_new_message, name="new-message")
]
