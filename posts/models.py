from django.db import models


class Post(models.Model):
    page = models.ForeignKey('pages.Page', verbose_name="Post page", on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(verbose_name="Post content", max_length=180)
    reply_to = models.ForeignKey('posts.Post', verbose_name="Post replies to", on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name='replies')
    likes = models.ManyToManyField('users.User', verbose_name="Post likes", related_name="liked_posts", blank=True)
    created_at = models.DateTimeField(verbose_name="Post date of creation", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Post update date", auto_now=True)
