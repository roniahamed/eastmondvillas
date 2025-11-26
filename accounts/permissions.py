from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsAdmin(BasePermission):
    """
    Custom permission to only allow users with 'admin' role to access the view.
    Assumes the User model has a 'role' attribute.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'


class IsAdminOrManager(BasePermission):
    """
    Custom permission to only allow users with 'admin' or 'manager' roles to edit objects.
    Assumes the User model has a 'role' attribute.
    """

    def has_permission(self, request, view):
        # Allow read-only access for any request
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']
    
class IsAgentWithFullAccess(BasePermission):
    """
    Custom permission to allow users with 'agent' role full access,
    while others have read-only access.
    Assumes the User model has a 'role' attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.assigned_agent == request.user and request.user.permission == 'full_access'

class IsAssignedAgentReadOnly(BasePermission):
    """
    Custom permission to allow only the assigned agent to have read-only access
    to the object. No write permissions are granted.
    Assumes the User model has a 'role' attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.assigned_agent == request.user
        return False


class IsOwnerOrAdminOrManager(BasePermission):

    message = "You do not have permission to view or edit this booking."

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.role in ['admin', 'manager']:
            return True
        
        return obj.user == request.user
    
class IsAgentOrAdminOrManager(BasePermission):
    """
    Custom permission to allow users with 'agent', 'admin', or 'manager' roles access.
    Assumes the User model has a 'role' attribute.
    """
    message = "You do not have permission to access this resource."

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.role in ['agent', 'admin', 'manager']:
            return True
        return False 
    
class IsAgent(BasePermission):
    """
    Custom permission to only allow users with 'agent' role to access the view.
    Assumes the User model has a 'role' attribute.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'agent'