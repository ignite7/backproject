"""
Permission auths.
"""

# Django REST framework
from rest_framework.permissions import BasePermission

# Modules
from api.auths.utils import get_authentication


class CheckOwner(BasePermission):
    """
    Check owner permission
    """

    message = 'Not authorized for this action.'

    def has_permission(self, request, view):
        """
        Check the user is the
        owner.
        """

        if not request.user.is_authenticated:
            return False

        if request.user.username != get_authentication(request).username:
            return False

        return True


class CheckVerifiedEmail(BaseException):
    """
    Check the user has the email confirmed.
    """

    message = 'Email verification not confirmed.'

    def has_permission(self, request, view):
        """
        Check email verification.
        """

        if not request.user.verified_email:
            return False

        return True
