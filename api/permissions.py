from rest_framework import permissions


class MotsditsPermissions(permissions.BasePermission):
    """Permissions specific to the MotDit endpoint"""

    def has_object_permission(self, request, view, obj):
        '''Mots-dits cannot be deleted via the API'''
        if request.method != 'DELETE':
            return True


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.created_by == request.user
