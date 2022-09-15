import jwt
from django.shortcuts import get_object_or_404
from rest_framework import authentication

from django.conf import settings
from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        request.user = None

        jwt_token = request.headers.get("Authorization", None)

        if not jwt_token:
            return None

        payload = jwt.decode(jwt_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

        username = payload.get("username")

        user = get_object_or_404(User, username=username)

        return user, jwt_token
