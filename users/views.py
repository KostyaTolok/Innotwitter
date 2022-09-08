from datetime import timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.filters import UserFilter
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer, LoginSerializer, BlockUserSerializer
from users.services import change_user_block_status, generate_token


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'register': RegisterSerializer,
        'login': LoginSerializer,
        'change_user_block_status': BlockUserSerializer
    }
    permission_classes = {
        'list': (AllowAny(), ),
        'retrieve': (AllowAny(), ),
        'register': (AllowAny(), ),
        'login': (AllowAny(), )
    }
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter
    default_serializer_class = UserSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return self.permission_classes.get(self.action, [AllowAny()])

    @action(detail=False, methods=["post"], url_path="change-block")
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

        username = request.data.get("username")

        user = User.objects.filter(username=username).first()

        token = generate_token(username, user.role, timedelta(minutes=60))

        return Response({"token": token}, status.HTTP_200_OK)
