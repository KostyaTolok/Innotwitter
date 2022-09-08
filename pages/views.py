from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from pages.filters import PageFilter
from pages.models import Page, Tag
from pages.serializers import PageSerializer, PageDetailSerializer, TagSerializer, AcceptFollowSerializer
from pages.services import add_user_to_followers, remove_user_from_followers, accept_follow_request, \
    accept_all_follow_requests
from users.serializers import UserSerializer


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

        message, status_code = add_user_to_followers(page, user)
        return Response(message, status_code)

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        user = request.user

        page = self.get_object()

        message, status_code = remove_user_from_followers(page, user)
        return Response(message, status_code)

    @action(detail=True, methods=["get"], url_path="follow-requests")
    def get_follow_requests(self, request, pk=None):
        page = self.get_object()
        serializer = UserSerializer(data=page.follow_requests, many=True)
        serializer.is_valid()
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="accept-follow")
    def accept_follow_request(self, request, pk=None):
        page = self.get_object()

        message, status_code = accept_follow_request(page, request.data)
        return Response(message, status_code)

    @action(detail=True, methods=["post"], url_path="accept-all-follows")
    def accept_all_follow_requests(self, request, pk=None):
        page = self.get_object()

        message, status_code = accept_all_follow_requests(page)
        return Response(message, status_code)


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
