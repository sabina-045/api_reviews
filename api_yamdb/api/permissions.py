from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrAuthenticatedOrReadOnly(BasePermission):
    """Разрешение анонимам просматривать список объектов,
    только авторизованным создавать объекты,
    только автору или админу редактировать и удалять объект."""
    def has_permission(self, request, view):

        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return obj.author == request.user or request.user.is_admin


class StaffOnly(BasePermission):
    """Разрешение модератору на изменеие или удаление
    комментариев или отзывов."""
    def has_permission(self, request, view):

        return request.user.is_staff

'''
class ReadOrAdminOnly(BasePermission):
    """Доступ админу к действиям над объектом."""
    def has_permission(self, request, view):

        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):

        return request.user.is_admin
'''

class ReadOrAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))
    
# переписал, сделал так: сейф методы или (и дальше двойное условие
# пользователь должен быть авторизован (чтоб через апи создавать изменять и удалять)
# и при этом иметь статус админа или суперюзера)
