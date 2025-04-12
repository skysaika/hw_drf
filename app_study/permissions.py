from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()

class NotModerator(BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name='moderators').exists()

class IsOwnerOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.groups.filter(name='moderators').exists()
