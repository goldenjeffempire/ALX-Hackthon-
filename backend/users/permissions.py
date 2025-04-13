from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    Permission to only allow users to view/edit their own profile
    or admins to view/edit any profile.
    """

    def has_object_permission(self, request, view, obj):
        # Allow administrators
        if request.user.is_staff or request.user.role == 'admin':
            return True

        # Allow users to access their own profile
        return obj.id == request.user.id


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to only allow admins to edit, but anyone can view.
    """

    def has_permission(self, request, view):
        # Allow any read-only request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for admins
        return request.user.is_staff or request.user.role == 'admin'
