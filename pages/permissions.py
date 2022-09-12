from rest_framework.permissions import BasePermission

from users.models import Roles


class IsPageOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsNotPageOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner != request.user


class IsPageNotBlocked(BasePermission):

    def has_object_permission(self, request, view, obj):
        return not obj.is_blocked_permanently and not obj.unblock_date


class IsPageNotBlockedOrIsAdminOrModerator(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role in (Roles.ADMIN, Roles.MODERATOR) \
               or not obj.is_blocked_permanently and not obj.unblock_date


class IsPageNotPrivateOrIsOwnerOrAdminOrModerator(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role in (Roles.ADMIN, Roles.MODERATOR) or (obj.owner == request.user) or not obj.is_private
