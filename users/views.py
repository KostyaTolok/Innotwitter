from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from Innotwitter.permissions import IsAuthenticated
from users.filters import UserFilter
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer, LoginSerializer
from users.services import register_user, login_user


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_classes = {
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'register': RegisterSerializer,
        'login': LoginSerializer
    }
    permission_classes = {
        'list': [IsAuthenticated()],
        'retrieve': [IsAuthenticated()],
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

    @action(detail=False, methods=["post"])
    def register(self, request):
        return register_user(request.data)

    @action(detail=False, methods=["post"])
    def login(self, request):
        return login_user(request.data)
