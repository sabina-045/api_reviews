from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrAuthenticatedOrReadOnly(BasePermission):
    """Разрешение анонимам просматривать список объектов,
    только авторизованным создавать объекты,
    только автору редактировать и удалять объект."""
    def has_permission(self, request, view):

        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return obj.author == request.user

