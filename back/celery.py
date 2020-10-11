"""
Celery
"""

# Celery
from __future__ import absolute_import
from celery import Celery

# Utilities
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')

app = Celery('back')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
