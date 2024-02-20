from rest_framework import permissions

class IsSupplierOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 'Потребитель':
            return True
        return request.method in permissions.SAFE_METHODS

class IsConsumerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 'Поставщик':
            return True
        return request.method in permissions.SAFE_METHODS
