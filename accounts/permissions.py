from rest_framework.permissions import BasePermission, SAFE_METHODS


class HasRole(BasePermission):
    """Allow safe methods for everyone. For unsafe methods require the user to
    have one of the allowed roles OR be staff.

    - Views can set `allowed_roles = ('admin','manager', 'agent')` to declare
      which roles may access unsafe methods.
    - If `allowed_roles` is not set, the default fallback requires the user to
      be staff or have role 'admin'.
    """

    def has_permission(self, request, view):
        # Allow safe methods
        if request.method in SAFE_METHODS:
            return True

        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False

        allowed = getattr(view, "allowed_roles", None)
        # If view doesn't declare allowed_roles: require staff or admin role
        if not allowed:
            return bool(getattr(user, "is_staff", False) or getattr(user, "role", None) == "admin")

        return getattr(user, "role", None) in allowed or bool(getattr(user, "is_staff", False))


class IsAdminOrReadOnly(BasePermission):
    """Simple helper: safe methods allowed, unsafe require admin role or staff."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False
        return getattr(user, "role", None) == "admin" or getattr(user, "is_staff", False)


class IsAdmin(BasePermission):
    """Allow access only to users with role 'admin' or is_staff=True.

    Use this for endpoints that must be restricted to administrators.
    """

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False
        return getattr(user, "role", None) == "admin" or getattr(user, "is_staff", False)
