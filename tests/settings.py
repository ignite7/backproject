"""
Test settings.
"""

# Back settings
from back.settings import *

# Base
DEBUG = False
SECRET_KEY = 'hjdasbdasSDHFJDAW"·N·RJSWIERN·J"IK$H$·RKFKSDFJSDCFSDJFSAKD"sad'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": ""
    }
}

# Password
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Email
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
