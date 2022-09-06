from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from pages.filters import PageFilter
from pages.models import Page, Tag
from pages.serializers import PageSerializer, PageDetailSerializer, TagSerializer, AcceptFollowSerializer
from pages.services import add_user_to_followers, remove_user_from_followers, serialize_follow_requests, \
    accept_follow_request, accept_all_follow_requests


class PageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': PageDetailSerializer,
        'retrieve': PageDetailSerializer,
        'create': PageSerializer,
        'update': PageSerializer,
        'destroy': PageSerializer,
        'accept_follow_request': AcceptFollowSerializer
    }
    queryset = Page.objects.all()
    default_serializer_class = PageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PageFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user = request.user

        page = self.get_object()

        return add_user_to_followers(page, user)

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        user = request.user

        page = self.get_object()

        return remove_user_from_followers(page, user)

    @action(detail=True, methods=["get"], url_path="follow-requests")
    def get_follow_requests(self, request, pk=None):
        page = self.get_object()

        return serialize_follow_requests(page.follow_requests)

    @action(detail=True, methods=["post"], url_path="accept-follow")
    def accept_follow_request(self, request, pk=None):
        page = self.get_object()

        return accept_follow_request(page, request.data)

    @action(detail=True, methods=["post"], url_path="accept-all-follows")
    def accept_all_follow_requests(self, request, pk=None):
        page = self.get_object()

        return accept_all_follow_requests(page)


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
