import logging
import os
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from Innotwitter.permissions import IsAdmin
from Innotwitter.services import upload_image
from users.filters import UserFilter
from users.models import User
from users.permissions import IsSameUser
from users.serializers import UserSerializer, RegisterSerializer, LoginSerializer, BlockUserSerializer, \
    UpdateUserInfoSerializer
from users.services import change_user_block_status, generate_token

logger = logging.getLogger(__name__)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'register': RegisterSerializer,
        'login': LoginSerializer,
        'change_user_block_status': BlockUserSerializer,
        'update': UpdateUserInfoSerializer
    }
    permission_classes = {
        'list': (IsAdmin(),),
        'retrieve': (IsAdmin(),),
        'register': (AllowAny(),),
        'login': (AllowAny(),),
        'change_user_block_status': (IsAdmin(),),
        'update': (IsSameUser(),)
    }
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter
    default_serializer_class = UserSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return self.permission_classes.get(self.action, (AllowAny(),))

    def perform_update(self, serializer):
        user = serializer.save()
        user_image = self.request.FILES.get("image", None)
        if user_image:
            try:
                user_image_key = os.path.join("users", str(user.id))
                upload_image(user_image, user_image_key)
                serializer.save(image=user_image_key)
            except Exception as error:
                logger.error(error)

    @action(detail=False, methods=["post"], url_path="change-block", url_name="change_user_block_status")
    def change_user_block_status(self, request, pk=None):
        serializer = BlockUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message, status_code = change_user_block_status(serializer.data["user_id"])
        return Response(message, status_code)

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("User registered", status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")

        user = get_object_or_404(User, username=username)

        token = generate_token(username, user.role, timedelta(days=60))

        return Response({"token": token}, status.HTTP_200_OK)
