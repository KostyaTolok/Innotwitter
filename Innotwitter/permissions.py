from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        jwt_token = request.headers.get("Authorization", None)

        return jwt_token is not None
