from rest_framework.permissions import BasePermission


class IsAuthenticatedWithServiceToken(BasePermission):
    def has_permission(self, request, view):
        '''
        Overrides the has_permission function in BasePermission
        '''
        return (
            request.user
            and hasattr(request.user, 'username')
            and request.user.username.startswith('service-')
            and hasattr(request.auth, 'key')
        )
