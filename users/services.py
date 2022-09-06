from datetime import datetime, timedelta
import jwt
from rest_framework import status
from rest_framework.response import Response

from Innotwitter.settings import JWT_SECRET_KEY
from users.models import User
from users.serializers import RegisterSerializer


def change_user_block_status(user_id):
    if user_id is None:
        return Response("User id isn't provided", status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(id=user_id).prefetch_related("pages").first()

    if user is None:
        return Response("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)

    if user.is_blocked:
        user.is_blocked = False
        user.save()
        return Response("User unblocked", status=status.HTTP_200_OK)
    else:
        user.is_blocked = True
        for page in user.pages.all():
            page.is_blocked_permanently = True
        user.save()
        return "User blocked", status.HTTP_200_OK


def register_user(user_data):
    serializer = RegisterSerializer(data=user_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return "User registered", status.HTTP_200_OK


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
