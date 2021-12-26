from chat import views
from django.urls import path
# https://channels.readthedocs.io/en/stable/introduction.html

app_name = "Chat"
urlpatterns = [
    path("", views.index, name="chat")
]
