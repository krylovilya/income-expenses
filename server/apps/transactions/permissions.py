from rest_framework import permissions


class RequestUserIsObjectOwnerPermission(permissions.BasePermission):
    """Проверяет, есть ли у пользователя доступ к объекту"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
