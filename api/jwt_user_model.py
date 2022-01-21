from django.contrib.auth.models import User
from rest_framework_simplejwt.models import TokenUser


class CustomJWTUser(TokenUser, User):
    def groups(self):
        return TokenUser.groups(self)

    def user_permissions(self):
        return TokenUser.user_permissions(self)
