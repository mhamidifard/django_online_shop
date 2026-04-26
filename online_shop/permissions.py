from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = "You must be an admin."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.is_staff
                or request.user.groups.filter(name='admin').exists()
            )
        )
