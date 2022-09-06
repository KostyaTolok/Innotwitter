from rest_framework import status
from rest_framework.response import Response

from posts.serializers import PostDetailSerializer


def change_post_like_status(post, user):
    if post.likes.contains(user):
        post.likes.remove(user)
        return Response("Like removed", status=status.HTTP_200_OK)
    else:
        post.likes.add(user)
        return Response("Post liked", status=status.HTTP_200_OK)


def serialize_posts(posts):
    serializer = PostDetailSerializer(data=posts, many=True)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)