from rest_framework import viewsets, mixins

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        query_dict = {key: value for key, value in self.request.query_params.items() if value}
        filter_dict = {}

        for key, value in query_dict.items():
            if key == "username":
                filter_dict["username__icontains"] = value
            if key == "title":
                filter_dict["title__icontains"] = value

        queryset = User.objects.filter(**filter_dict)
        return queryset


