import django_filters
from django_filters import rest_framework as filters


class PostFilter(django_filters.FilterSet):
    page = filters.UUIDFilter(field_name="page__uuid")
    like = filters.NumberFilter(field_name="likes")
