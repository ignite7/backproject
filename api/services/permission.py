"""
Permission services.
"""

# Django REST framework
from rest_framework.permissions import BasePermission, IsAuthenticated

# Models
from models.models import Restricts

# Modules
from api.auths.utils import get_authentication

# Permissions
from api.auths.permission import CheckOwner, CheckVerifiedEmail

# Tasks
from api.services.tasks import clean_ip_addrs


class CheckRequestPerHour(BasePermission):
    """
    Check request per hour permission.
    """

    message = 'Max request allowed by an anonymous user is three times per hour.'

    def has_permission(self, request, view):
        """
        Check if the user if authenticated
        otherwise check if the anonymous user
        only can make more than 3 requests per
        hour.
        """

        clean_ip_addrs.delay()

        try:
            if request.user.is_authenticated or get_authentication(request).is_authenticated:
                permissions = [
                    IsAuthenticated(),
                    CheckOwner(),
                    CheckVerifiedEmail()
                ]
                execute_permissions = [
                    permission.has_permission(request, view) for permission in permissions
                ]

                count_success_permissions = 0

                for check_permission in execute_permissions:
                    if check_permission:
                        count_success_permissions += 1

                if count_success_permissions != 3:
                    return False

                return True

            ip_addrs = Restricts.objects.filter(
                ip_remote_addr=request.META['REMOTE_ADDR']
            )

            if ip_addrs.exists():
                for ip_addr in ip_addrs:
                    ip_addr.requests += 1
                    ip_addr.save()

            else:
                ip_addrs.create(
                    ip_remote_addr=request.META['REMOTE_ADDR'],
                    requests=1
                )

            for ip_addr in ip_addrs:
                if ip_addr.requests > 3:
                    return False

            return True

        except (KeyError, TypeError):
            return False
