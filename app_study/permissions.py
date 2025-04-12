from rest_framework import permissions

# Владелец
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

# Модератор
class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()

# Не модератор
class NotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name='moderators').exists()

# Владелец или модератор
class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.groups.filter(name='moderators').exists()
