from rest_framework.permissions import (
    BasePermission,
    IsAuthenticatedOrReadOnly,
    SAFE_METHODS,
)


class IsAdminUserOrReadOnly(BasePermission):
    """
    The request is Admin as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or request.user and request.user.is_staff
        )


class IsBlogOwnerOrReadOnly(BasePermission):
    """
    The request is Owner of Blog as a user, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True

        if request.user.is_staff:
            return True

        return request.method in SAFE_METHODS


class IsCommentOwnerOrReadOnly(BasePermission):
    """
    The request is Owner of Comment as a user, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True

        if request.user.is_staff:
            return True

        return request.method in SAFE_METHODS
