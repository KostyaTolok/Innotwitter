from rest_framework.permissions import BasePermission

from users.models import Roles


class IsPageOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsNotPageOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner != request.user


class IsAdminOrPageOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.role == Roles.ADMIN:
            return True

        return obj.owner == request.user


class IsPageNotPrivate(BasePermission):

    def has_object_permission(self, request, view, obj):
        return not obj.is_private


class IsPageNotBlocked(BasePermission):

    def has_object_permission(self, request, view, obj):
        return not obj.is_blocked_permanently and not obj.unblock_date
