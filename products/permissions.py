from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    message = "You must be seller."
    def has_permission(self, request, view):
        return request.user.groups.filter(name='seller').exists()

class IsSellerOwner(permissions.BasePermission):
    message = "You must be seller owner or admin."
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'seller'):
            return obj.seller == request.user

        if hasattr(obj, 'product') and hasattr(obj.product, 'seller'):
            return obj.product.seller == request.user

        return False