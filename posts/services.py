from rest_framework import status

from posts.models import Post


def change_post_like_status(post, user):
    if post.likes.contains(user):
        post.likes.remove(user)
        return "Like removed", status.HTTP_200_OK
    else:
        post.likes.add(user)
        return "Post liked", status.HTTP_200_OK


def get_news_feed(user):
    user_posts = Post.objects.filter(page__owner=user)

    follows = Post.objects.filter(page__followers=user)

    posts = user_posts | follows

    posts = posts.distinct().order_by("-created_at")

    return posts
