from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from pages.models import Page, Tag
from pages.serializers import PageDetailSerializer, PageListSerializer, TagSerializer


class PageListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PageListSerializer
    queryset = Page.objects.all()


class PageDetailViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = PageDetailSerializer
    queryset = Page.objects.all()

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user = request.user

        if user.is_blocked:
            return Response("User is blocked", status=status.HTTP_403_FORBIDDEN)

        page = self.get_object()

        if page.followers.contains(user):
            return Response("User already follows this page", status=status.HTTP_400_BAD_REQUEST)

        if page.follow_requests.contains(user):
            return Response("User already sent follow request to this page", status=status.HTTP_400_BAD_REQUEST)

        if page.unblock_date is not None:
            return Response("Page is blocked", status=status.HTTP_403_FORBIDDEN)

        if page.is_private:
            page.follow_requests.add(user)
            return Response("User added to follow requests", status=status.HTTP_200_OK)
        else:
            page.followers.add(user)
            return Response("User added to followers", status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        user = request.user

        if user.is_blocked:
            return Response("User is blocked", status=status.HTTP_403_FORBIDDEN)

        page = self.get_object()

        if not page.followers.contains(user):
            return Response("User doesn't follow this page", status=status.HTTP_400_BAD_REQUEST)

        if page.unblock_date is not None:
            return Response("Page is blocked", status=status.HTTP_403_FORBIDDEN)

        page.followers.remove(user)
        return Response("User removed from followers", status=status.HTTP_200_OK)


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
