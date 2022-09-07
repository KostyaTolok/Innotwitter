import jwt
from rest_framework import authentication

from Innotwitter.settings import JWT_SECRET_KEY
from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        jwt_token = request.headers.get("Authorization", None)
        if not jwt_token:
            return None

        payload = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=['HS256'])

        username = payload.get("username", None)

        user = User.objects.filter(username=username).first()

        return user, jwt_token
