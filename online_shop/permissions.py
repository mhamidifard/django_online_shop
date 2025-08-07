from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = "You must be an admin."
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='admin').exists()