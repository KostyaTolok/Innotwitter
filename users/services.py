from datetime import datetime, timedelta

import jwt
from rest_framework import status

from Innotwitter.settings import JWT_SECRET_KEY
from users.models import User


def change_user_block_status(user_id):
    if user_id is None:
        return "User id isn't provided", status.HTTP_400_BAD_REQUEST

    user = User.objects.filter(id=user_id).prefetch_related("pages").first()

    if user is None:
        return "User doesn't exist", status.HTTP_400_BAD_REQUEST

    user.is_blocked = not user.is_blocked
    for page in user.pages.all():
        page.is_blocked_permanently = not page.is_blocked_permanently
        page.save()
    user.save()

    if user.is_blocked:
        return "User blocked", status.HTTP_200_OK
    else:
        return "User unblocked", status.HTTP_200_OK


def generate_token(username, role, expires_in):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + expires_in,
        "iat": datetime.utcnow()
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
