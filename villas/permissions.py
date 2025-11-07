from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminAgentManager(BasePermission):
    """Allow safe methods for everyone. For modifying actions only allow users with role admin/manager/agent or is_staff."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return False
        return getattr(user, 'role', None) in ('admin', 'manager', 'agent') or getattr(user, 'is_staff', False)


class IsBookingOwnerOrManager(BasePermission):
    """Allow booking modification to the booking owner (user) or manager/admin roles."""

    def has_permission(self, request, view):
        # Allow create for authenticated users
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        # other non-object actions require auth
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # safe methods allowed
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # manager or admin can modify any booking
        if getattr(user, 'role', None) in ('admin', 'manager') or getattr(user, 'is_staff', False):
            return True
        # the booking owner (if present) can modify
        if hasattr(obj, 'user') and obj.user and obj.user == user:
            return True
        return False
