from rest_framework import permissions


class OwnerAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST' and request.user.is_authenticated:
            return obj.author == request.user
        elif (
                request.method == 'PUT' and request.user.is_superuser
                or obj.author == request.user or request.user.is_moderator
        ):
            return True
        elif (
                request.method == 'DELETE' and request.user.is_superuser
                or obj.author == request.user or request.user.is_moderator
                or request.user.is_admin
        ):
            return True
        else:
            return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True


class OwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (
                request.user.is_authenticated
                and (
                    obj.author == request.user
                    or request.user.is_admin
                    or request.user.is_moderator
                )
        ):
            return True
