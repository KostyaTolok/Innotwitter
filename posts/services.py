from rest_framework import status

from posts.models import Post
from posts.serializers import PostDetailSerializer


def change_post_like_status(post, user):
    if post.likes.contains(user):
        post.likes.remove(user)
        return "Like removed", status.HTTP_200_OK
    else:
        post.likes.add(user)
        return "Post liked", status.HTTP_200_OK


def get_news_feed(user):
    user_posts = Post.objects.filter(page__owner=user, page__is_blocked_permanently=False, page__unblock_date=None)

    follows = Post.objects.filter(page__followers=user)

    posts = user_posts | follows

    posts = posts.distinct().order_by("-created_at")

    return posts


def get_liked_posts(user):
    liked_posts = Post.objects.filter(likes=user, page__is_blocked_permanently=False, page__unblock_date=None)

    serializer = PostDetailSerializer(data=liked_posts, many=True)
    serializer.is_valid()

    return serializer.data


def get_page_followers_emails(page):
    emails = []

    for follower in page.followers.all():
        if not follower.is_blocked:
            emails.append(follower.email)

    return emails
