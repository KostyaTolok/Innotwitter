from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from pages.models import Page, Tag
from pages.serializers import PageSerializer, PageDetailSerializer, TagSerializer
from users.serializers import UserSerializer


class PageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = PageDetailSerializer
    queryset = Page.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PageDetailSerializer
        else:
            return PageSerializer

    def get_queryset(self):
        query_dict = {key: value for key, value in self.request.query_params.items() if value}
        filter_dict = {}

        for key, value in query_dict.items():
            if key == "name":
                filter_dict["name__icontains"] = value
            if key == "uuid":
                filter_dict["uuid"] = value
            if key == "tag":
                filter_dict["tags__name__icontains"] = value

        queryset = Page.objects.filter(**filter_dict)
        return queryset

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user = request.user

        if user.is_blocked:
            return Response("User is blocked", status=status.HTTP_403_FORBIDDEN)

        page = self.get_object()

        if page.unblock_date is not None:
            return Response("Page is blocked", status=status.HTTP_403_FORBIDDEN)

        if page.followers.contains(user):
            return Response("User already follows this page", status=status.HTTP_400_BAD_REQUEST)

        if page.follow_requests.contains(user):
            return Response("User already sent follow request to this page", status=status.HTTP_400_BAD_REQUEST)

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

        if page.unblock_date is not None:
            return Response("Page is blocked", status=status.HTTP_403_FORBIDDEN)

        if not page.followers.contains(user):
            return Response("User doesn't follow this page", status=status.HTTP_400_BAD_REQUEST)

        page.followers.remove(user)
        return Response("User removed from followers", status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="follow-requests")
    def get_follow_requests(self, request, pk=None):
        page = self.get_object()
        serializer = UserSerializer(data=page.follow_requests, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
