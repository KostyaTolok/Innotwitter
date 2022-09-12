from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from pages.models import Page


class IsAllowedToCreatePost(BasePermission):
    def has_permission(self, request, view):
        page_uuid = request.data.get("page")
        page = get_object_or_404(Page, uuid=page_uuid)
        return request.user == page.owner and not page.is_blocked_permanently and not page.unblock_date


class IsPostPageOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.page.owner


class IsPostPageNotBlocked(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.page.is_blocked_permanently and not obj.page.unblock_date
