"""
Commons models.
"""

# Django
from django.db import models


class Commons(models.Model):
    """
    This class it's gonna handle to inherit
    the common info to the other classes.
    """

    created_at = models.DateTimeField(
        name='created_at',
        auto_now_add=True,
        help_text='When it has been created.'
    )

    modified_at = models.DateTimeField(
        name='modified_at',
        auto_now=True,
        help_text='When it has been modified.'
    )

    is_used = models.BooleanField(
        default=True,
        help_text='By default everything will be active.'
    )

    class Meta:
        """
        Meta class.
        """

        abstract = True
        get_latest_by = 'created_at',
        ordering = [
            '-created_at',
            '-modified_at'
        ]
