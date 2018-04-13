from rest_framework import permissions


# User authentication required for these actions
class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in [
            'partial_update', 'logout',
            'changePassword', 'list', 'faq'
        ]:
            return request.user.is_authenticated
        if view.action in [
            'create',  'checkDuplicateEmail', 'checkDuplicateUsername',
            'login', 'resetPassword',
        ]:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj or request.user
        return False
