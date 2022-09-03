from rest_framework import viewsets, mixins

from posts.models import Post
from posts.serializers import PostSerializer


class PostListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
