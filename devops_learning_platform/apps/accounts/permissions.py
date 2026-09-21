"""Custom DRF permissions."""
from rest_framework.permissions import BasePermission


class IsPremiumUser(BasePermission):
    """Only premium users can access this endpoint."""
    message = 'This feature requires a premium account.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_premium)


class IsOwnerOrReadOnly(BasePermission):
    """Object-level permission: only the owner can edit."""
    def has_object_permission(self, request, view, obj):
        from rest_framework.permissions import SAFE_METHODS
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user or hasattr(obj, 'user') and obj.user == request.user
