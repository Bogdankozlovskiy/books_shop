from rest_framework_simplejwt.models import TokenUser
from django.contrib.auth.models import User


class CustomJWTUser(TokenUser, User):
    pass
