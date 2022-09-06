from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from Innotwitter.permissions import IsAuthenticated
from users.filters import UserFilter
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer, LoginSerializer, BlockUserSerializer
from users.services import register_user, login_user, change_user_block_status


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'register': RegisterSerializer,
        'login': LoginSerializer,
        'change_user_block_status': BlockUserSerializer
    }
    permission_classes = {
        'list': [AllowAny()],
        'retrieve': [AllowAny()],
        'register': [AllowAny()],
        'login': [AllowAny()]
    }
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter
    default_serializer_class = UserSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return self.permission_classes.get(self.action, [AllowAny()])

    @action(detail=True, methods=["post"], url_path="change-block")
    def change_user_block_status(self, request, pk=None):
        return change_user_block_status(pk)

    @action(detail=False, methods=["post"])
    def register(self, request):
        message, status_code = register_user(request.data)
        return Response(message, status_code)

    @action(detail=False, methods=["post"])
    def login(self, request):
        return login_user(request.data)
