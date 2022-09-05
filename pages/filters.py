import django_filters
from django_filters import rest_framework as filters


class PageFilter(django_filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    uuid = filters.UUIDFilter()
    tag = filters.CharFilter(field_name="tags__name", lookup_expr="icontains")
