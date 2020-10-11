"""
Versions back.
"""

# Django REST Framework
from rest_framework.versioning import AcceptHeaderVersioning


class APIVersion(AcceptHeaderVersioning):
    """
    API Version.
    """

    default_version = 'v1'
    allowed_versions = ['v1']
    version_param = 'version'
