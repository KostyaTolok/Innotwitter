import asyncio

from django.shortcuts import get_object_or_404
from rest_framework import status

from Innotwitter.producer import publish_message
from Innotwitter.utils import MessageTypes
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

        send_update_followers_count_message(page.uuid, page.followers.count())

        return "User added to followers", status.HTTP_200_OK


def remove_user_from_followers(page, user):
    if not page.followers.contains(user):
        return "User doesn't follow this page", status.HTTP_400_BAD_REQUEST

    page.followers.remove(user)

    send_update_followers_count_message(page.uuid, page.followers.count())

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

    send_update_followers_count_message(page.uuid, page.followers.count())

    return "User added to followers", status.HTTP_200_OK


def accept_all_follow_requests(page):
    follow_requests = page.follow_requests.all()

    for user in follow_requests:

        if user.is_blocked:
            continue

        page.follow_requests.remove(user)
        page.followers.add(user)

    send_update_followers_count_message(page.uuid, page.followers.count())

    return "All follow requests accepted", status.HTTP_200_OK


def send_create_page_statistics_message(page_uuid):
    message = {'uuid': str(page_uuid), 'type': MessageTypes.CREATE.name}

    asyncio.run(publish_message(message))


def send_destroy_page_statistics_message(page_uuid):
    message = {'uuid': str(page_uuid), 'type': MessageTypes.DELETE.name}

    asyncio.run(publish_message(message))


def send_update_followers_count_message(page_uuid, followers_count):
    message = {'uuid': str(page_uuid), 'type': MessageTypes.UPDATE.name,
               "followers_count": followers_count}

    asyncio.run(publish_message(message))

