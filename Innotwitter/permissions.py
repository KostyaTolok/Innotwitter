from rest_framework.permissions import BasePermission

from users.models import Roles


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Roles.ADMIN


class IsAdminOrModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.role in (Roles.ADMIN, Roles.MODERATOR)
