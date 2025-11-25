from rest_framework.permissions import BasePermission


class UserPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:
            return bool(request.user and (request.user.is_admin or request.user.is_staff))
