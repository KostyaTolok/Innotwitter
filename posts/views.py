from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from posts.filters import PostFilter
from posts.models import Post
from posts.serializers import PostSerializer, PostDetailSerializer
from posts.services import change_post_like_status, serialize_posts


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': PostDetailSerializer,
        'retrieve': PostDetailSerializer,
        'create': PostSerializer,
        'update': PostSerializer,
        'destroy': PostSerializer
    }
    default_serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

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

        post = self.get_object()

        return change_post_like_status(post, user)

    @action(detail=False, methods=["get"], url_path="liked-posts")
    def get_liked_posts(self, request):
        user = request.user

        posts = self.get_queryset().filter(likes=user.id)
        return serialize_posts(posts)
