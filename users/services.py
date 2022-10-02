from datetime import datetime, timedelta

import jwt
from django.shortcuts import get_object_or_404
from rest_framework import status

from django.conf import settings
from users.models import User


def change_user_block_status(user_id):
    if user_id is None:
        return "User id isn't provided", status.HTTP_400_BAD_REQUEST

    user = get_object_or_404(User, id=user_id)

    user.is_blocked = not user.is_blocked
    for page in user.pages.all():
        page.is_blocked_permanently = not page.is_blocked_permanently
        page.save()
    user.save()

    if user.is_blocked:
        return "User blocked", status.HTTP_200_OK
    else:
        return "User unblocked", status.HTTP_200_OK


def generate_token(username, role, expires_in=timedelta(minutes=settings.ACCESS_TOKEN_DEFAULT_EXPIRE_MINUTES)):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + expires_in,
        "iat": datetime.utcnow()
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
