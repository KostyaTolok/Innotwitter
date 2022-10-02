import django_filters
from django_filters import rest_framework as filters


class UserFilter(django_filters.FilterSet):
    username = filters.CharFilter(lookup_expr="icontains")
    title = filters.CharFilter(lookup_expr="icontains")
