from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from Innotwitter.permissions import IsAdmin
from posts.filters import PostFilter
from posts.models import Post
from posts.permissions import IsPostPageOwner, IsPostPageNotBlocked, IsAllowedToCreatePost
from posts.serializers import PostSerializer, PostDetailSerializer
from posts.services import change_post_like_status, get_news_feed, get_liked_posts, \
    send_update_posts_count_message, send_email_notification_to_followers


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': PostDetailSerializer,
        'retrieve': PostDetailSerializer,
        'create': PostSerializer,
        'update': PostSerializer,
        'destroy': PostSerializer,
        'get_liked_posts': PostDetailSerializer,
        'get_news_feed': PostDetailSerializer
    }
    permission_classes = {
        'list': (IsAdmin(),),
        'retrieve': (IsAuthenticated(), IsPostPageNotBlocked()),
        'create': (IsAllowedToCreatePost(),),
        'update': (IsPostPageOwner(), IsPostPageNotBlocked(),),
        'destroy': (IsPostPageOwner(), IsPostPageNotBlocked(),),
        'change_like_status': (IsAuthenticated(), IsPostPageNotBlocked(),),
        'get_liked_posts': (IsAuthenticated(),),
        'get_news_feed': (IsAuthenticated(),)
    }
    default_serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return self.permission_classes.get(self.action, (AllowAny(),))

    def perform_create(self, serializer):
        post = serializer.save()
        page = post.page

        send_email_notification_to_followers(page)
        send_update_posts_count_message(page.uuid, page.posts.count())

    @action(detail=True, methods=["post"], url_path="change-like", url_name="change_like_status")
    def change_like_status(self, request, pk=None):
        user = request.user

        post = self.get_object()

        message, status_code = change_post_like_status(post, user)

        return Response(message, status_code)

    @action(detail=False, methods=["get"], url_path="liked-posts", url_name="get_liked_posts")
    def get_liked_posts(self, request):
        liked_posts = get_liked_posts(request.user)

        return Response(liked_posts, status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="news-feed", url_name="get_news_feed")
    def get_news_feed(self, request):
        posts = get_news_feed(request.user)
        serializer = PostDetailSerializer(posts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
