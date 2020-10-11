"""
Tasks services.
"""

# Django REST framework
from rest_framework import status

# Celery
from celery import shared_task

# Models
from models.models import Restricts

# Modules
from api.services.commons import status_code

# Utilities
import datetime


@shared_task
def clean_ip_addrs():
    """
    Clean the list of remote
    addresses when its called.
    """

    now = datetime.datetime.now().strftime('%H')
    ip_addrs = Restricts.objects.filter(requests__gte=3, is_used=True)

    for ip_addr in ip_addrs:
        offset = ip_addr.created_at + datetime.timedelta(hours=1)

        if offset.strftime('%H') == now:
            ip_addr.delete()

    return status_code(status=status.HTTP_200_OK)
