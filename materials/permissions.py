from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ только модераторам.
    """

    def has_permission(self, request, view):
        # Проверяем, если пользователь аутентифицирован и принадлежит группе 'модераторы'
        return request.user.is_authenticated and request.user.groups.filter(name='модераторы').exists()

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать и удалять только владельцу объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешить доступ на чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить изменение и удаление только владельцу
        return obj.user == request.user