from django.contrib.auth.models import User
from rest_framework_simplejwt.models import TokenUser


class CustomJWTUser(TokenUser, User):
    pass
