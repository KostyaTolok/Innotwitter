from rest_framework.permissions import BasePermission

from users.models import Roles


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated()


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Roles.ADMIN


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Roles.MODERATOR


class IsAdminOrModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.role in (Roles.ADMIN, Roles.MODERATOR)
