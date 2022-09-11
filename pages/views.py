from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Innotwitter.permissions import IsAdmin, IsAdminOrModerator
from pages.filters import PageFilter
from pages.models import Page, Tag
from pages.permissions import IsPageOwner, IsPageNotPrivate, IsPageNotBlocked, IsNotPageOwner
from pages.serializers import PageSerializer, PageDetailSerializer, TagSerializer, AcceptFollowSerializer, \
    BlockPageSerializer, PageListSerializer
from pages.services import add_user_to_followers, remove_user_from_followers, accept_follow_request, \
    accept_all_follow_requests
from users.serializers import UserSerializer


class PageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': PageListSerializer,
        'retrieve': PageDetailSerializer,
        'create': PageSerializer,
        'update': PageSerializer,
        'destroy': PageSerializer,
        'accept_follow_request': AcceptFollowSerializer,
        'block_page': BlockPageSerializer
    }
    permission_classes = {
        'list': (IsAuthenticated(),),
        'retrieve': (IsAuthenticated(), (IsPageNotBlocked | IsAdminOrModerator)(), (IsPageNotPrivate | IsPageOwner)(),),
        'create': (IsAuthenticated(),),
        'update': (IsPageOwner(), IsPageNotBlocked(),),
        'destroy': (IsPageOwner(), IsPageNotBlocked(),),
        'follow': (IsNotPageOwner(), IsPageNotBlocked(),),
        'unfollow': (IsNotPageOwner(), IsPageNotBlocked(),),
        'get_follow_requests': (IsPageOwner(), IsPageNotBlocked(),),
        'accept_follow_request': (IsPageOwner(), IsPageNotBlocked(),),
        'accept_all_follow_requests': (IsPageOwner(), IsPageNotBlocked(),),
        'block_page': (IsAdminOrModerator(),),
        'unblock_page': (IsAdminOrModerator(),),
        'change_permanent_block_status': (IsAdmin(),),
    }
    queryset = Page.objects.all()
    default_serializer_class = PageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PageFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return self.permission_classes.get(self.action, (AllowAny(),))

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

    @action(detail=True, methods=["patch"], url_path="block-page")
    def block_page(self, request, pk=True):
        serializer = BlockPageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        page = self.get_object()
        unblock_date = serializer.data.get("unblock_date")
        page.unblock_date = unblock_date
        page.save()

        return Response(f"Page blocked", status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="unblock-page")
    def unblock_page(self, request, pk=None):
        page = self.get_object()
        page.unblock_date = None
        page.save()

        return Response("Page unblocked", status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], url_path="change-permanent-block")
    def change_permanent_block_status(self, request, pk=None):
        page = self.get_object()
        page.is_blocked_permanently = not page.is_blocked_permanently
        page.save()

        if page.is_blocked_permanently:
            return Response("Page blocked permanently", status.HTTP_200_OK)
        else:
            return Response("Page unblocked", status.HTTP_200_OK)


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
