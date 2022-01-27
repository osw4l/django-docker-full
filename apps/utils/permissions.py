from rest_framework.permissions import BasePermission
from apps.utils.exceptions import RegisterDisabledValidationError
from apps.utils.redis import client as redis


class IsCompanyUser(BasePermission):
    """
    Allows access only to company users.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'companyuser')


class IsCompanyOwner(BasePermission):
    """
    Allows access only to company owners.
    """

    def has_permission(self, request, view):
        return bool(request.user.companyuser.role == 'owner')


class IsRegisterEnabled(BasePermission):
    """
    Allows access when register allow_register=True
    """

    def has_permission(self, request, view):
        if not redis.get_json('setup').get('allow_register'):
            raise RegisterDisabledValidationError()
        return True

