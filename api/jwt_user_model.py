from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.models import TokenUser
from django.contrib.auth.models import User


class CustomJWTUser(TokenUser, User):
    def groups(self):
        return TokenUser.groups(self)

    def user_permissions(self):
        return TokenUser.user_permissions(self)


class MyCustomJWTAuthentication(JWTTokenUserAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES['JWT']
        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
