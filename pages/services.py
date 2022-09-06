from rest_framework import status
from rest_framework.response import Response

from pages.serializers import AcceptFollowSerializer
from users.models import User
from users.serializers import UserSerializer


def add_user_to_followers(page, user):
    if page.followers.contains(user):
        return Response("User already follows this page", status=status.HTTP_400_BAD_REQUEST)

    if page.follow_requests.contains(user):
        return Response("User already sent follow request to this page", status=status.HTTP_400_BAD_REQUEST)

    if page.is_private:
        page.follow_requests.add(user)
        return Response("User added to follow requests", status=status.HTTP_200_OK)
    else:
        page.followers.add(user)
        return Response("User added to followers", status=status.HTTP_200_OK)


def remove_user_from_followers(page, user):
    if not page.followers.contains(user):
        return Response("User doesn't follow this page", status=status.HTTP_400_BAD_REQUEST)

    page.followers.remove(user)
    return Response("User removed from followers", status=status.HTTP_200_OK)


def serialize_follow_requests(follow_requests):
    serializer = UserSerializer(data=follow_requests, many=True)
    serializer.is_valid()
    return Response(serializer.data, status=status.HTTP_200_OK)


def accept_follow_request(page, follow_request):
    serializer = AcceptFollowSerializer(data=follow_request)
    serializer.is_valid(raise_exception=True)

    user_id = serializer.data.get("user_id", None)

    if user_id is None:
        return Response("User id is not provided", status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(id=user_id).first()

    if user is None:
        return Response("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)

    if user.is_blocked:
        return Response("User is blocked", status=status.HTTP_403_FORBIDDEN)

    if not page.follow_requests.contains(user):
        return Response("User didn't send follow request", status=status.HTTP_400_BAD_REQUEST)

    page.follow_requests.remove(user)
    page.followers.add(user)
    return Response("User added to followers", status=status.HTTP_200_OK)


def accept_all_follow_requests(page):
    follow_requests = page.follow_requests.all()

    for user in follow_requests:

        if user.is_blocked:
            continue

        page.follow_requests.remove(user)
        page.followers.add(user)

    return Response("All follow requests accepted", status=status.HTTP_200_OK)