from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Разрешает доступ только админу.
    """
    message = 'Доступно только админу.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsSuperuser(permissions.BasePermission):
    """
    Разрешает доступ только суперпользователю.
    """
    message = 'Доступно только суперюзеру.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только админу, остальным чтение.
    """
    message = 'Изменить контент может только админ.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ только автору объекта, модератору или администратору.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user == obj.author
                or request.user.is_moderator
                or request.user.is_admin
            )
        return False
