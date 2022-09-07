from datetime import datetime, timedelta
import jwt
from rest_framework import status
from rest_framework.response import Response

from Innotwitter.settings import JWT_SECRET_KEY
from users.models import User
from users.serializers import RegisterSerializer


def register_user(user_data):
    serializer = RegisterSerializer(data=user_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response("User registered", status=status.HTTP_200_OK)


def login_user(user_data):
    username = user_data.get("username", None)
    password = user_data.get("password", None)

    if username is None:
        return Response("Username is required", status=status.HTTP_400_BAD_REQUEST)

    if password is None:
        return Response("Password is required", status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(username=username).first()

    if user is None:
        return Response("User not found", status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
        return Response("Password is incorrect", status=status.HTTP_400_BAD_REQUEST)

    token = generate_token(username, user.role, timedelta(minutes=60))

    response = Response("User signed in", status=status.HTTP_200_OK)
    response.data = {
        "token": token,
    }

    return response


def generate_token(username, role, expires_in):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + expires_in,
        "iat": datetime.utcnow()
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
