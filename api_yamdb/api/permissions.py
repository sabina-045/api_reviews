from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrAuthenticatedOrReadOnly(BasePermission):
    """Разрешение анонимам просматривать список объектов,
    только авторизованным создавать объекты,
    только автору редактировать и удалять объект."""
    def has_permission(self, request, view):

        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return obj.author == request.user


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ReadOnly(BasePermission):
    """Только чтение (анониму)"""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class UserOnly(BasePermission):
    """Доступ авторизированному пользователю."""
    def has_permission(self, request, view):
        return request.user.is_user


class ModeratorOnly(BasePermission):
    """Доступ модератору."""
    def has_permission(self, request, view):
        return request.user.is_moderator


class AdminOnly(BasePermission):
    """Доступ админу."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)


class StaffOnly(BasePermission):
    """Доступ модератору, админу, суперюзеру"""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser)


class AuthorOrReadOnly(BasePermission):
    """Разрешение анонимам просматривать список объектов,
    только авторизованным создавать объекты,
    только автору редактировать и удалять объект."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
