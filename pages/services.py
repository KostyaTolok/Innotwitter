import os.path

import boto3
from django.shortcuts import get_object_or_404
from rest_framework import status

from Innotwitter.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_ENDPOINT_URL, AWS_BUCKET_NAME
from pages.serializers import AcceptFollowSerializer
from users.models import User


def add_user_to_followers(page, user):
    if page.followers.contains(user):
        return "User already follows this page", status.HTTP_400_BAD_REQUEST

    if page.follow_requests.contains(user):
        return "User already sent follow request to this page", status.HTTP_400_BAD_REQUEST

    if page.is_private:
        page.follow_requests.add(user)
        return "User added to follow requests", status.HTTP_200_OK
    else:
        page.followers.add(user)
        return "User added to followers", status.HTTP_200_OK


def remove_user_from_followers(page, user):
    if not page.followers.contains(user):
        return "User doesn't follow this page", status.HTTP_400_BAD_REQUEST

    page.followers.remove(user)
    return "User removed from followers", status.HTTP_200_OK


def accept_follow_request(page, follow_request):
    serializer = AcceptFollowSerializer(data=follow_request)
    serializer.is_valid(raise_exception=True)

    user_id = serializer.data.get("user_id")

    user = get_object_or_404(User, id=user_id)

    if user.is_blocked:
        return "User is blocked", status.HTTP_400_BAD_REQUEST

    if not page.follow_requests.contains(user):
        return "User didn't send follow request", status.HTTP_400_BAD_REQUEST

    page.follow_requests.remove(user)
    page.followers.add(user)
    return "User added to followers", status.HTTP_200_OK


def accept_all_follow_requests(page):
    follow_requests = page.follow_requests.all()

    for user in follow_requests:

        if user.is_blocked:
            continue

        page.follow_requests.remove(user)
        page.followers.add(user)

    return "All follow requests accepted", status.HTTP_200_OK
