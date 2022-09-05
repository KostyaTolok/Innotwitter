from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post
from posts.serializers import PostSerializer, PostDetailSerializer


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PostDetailSerializer
        else:
            return PostSerializer

    def get_queryset(self):
        params = self.request.query_params
        page_uuid = params.get("page", None)

        if page_uuid is None:
            return Post.objects.all()
        else:
            return Post.objects.filter(page__uuid=page_uuid)

    @action(detail=True, methods=["post"], url_path="change-like")
    def change_like_status(self, request, pk=None):
        user = request.user

        if user.is_blocked:
            return Response("User is blocked", status=status.HTTP_403_FORBIDDEN)

        post = self.get_object()

        if post.likes.contains(user):
            post.likes.remove(user)
            return Response("Like removed", status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response("Post liked", status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="liked-posts")
    def get_liked_posts(self, request):
        user = request.user

        if user.is_blocked:
            return Response("User is blocked", status=status.HTTP_403_FORBIDDEN)

        posts = self.get_queryset().filter(likes=user.id)
        serializer = PostDetailSerializer(data=posts, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)