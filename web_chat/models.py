from django.db import models


class ChatMessage(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
