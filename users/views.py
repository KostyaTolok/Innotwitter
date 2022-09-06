from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins

from users.filters import UserFilter
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter



