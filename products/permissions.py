from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    message = "You must be seller."
    def has_permission(self, request, view):
        return request.user.groups.filter(name='seller').exists()

class IsSellerOwnerOrAdmin(permissions.BasePermission):
    message = "You must be seller owner or admin."
    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.groups.filter(name='admin').exists():
            return True

        if hasattr(obj, 'seller'):
            return obj.seller == request.user

        if hasattr(obj, 'product') and hasattr(obj.product, 'seller'):
            return obj.product.seller == request.user

        return False