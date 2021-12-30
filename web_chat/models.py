from django.db import models
from django.contrib.auth.models import User


class ChatMessage(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
