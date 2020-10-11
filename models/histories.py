"""
Models records
"""

# Models
from models.models import models, Commons, Users


class Histories(Commons):
    """
    This class it gonna handle to
    save the searches of the user
    when is logged.
    """

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        help_text='User info.'
    )

    service = models.CharField(
        max_length=25,
        help_text='Service.'
    )

    types = models.CharField(
        max_length=25,
        help_text='Type.'
    )

    search = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        help_text='Search field.'
    )

    year = models.IntegerField(
        null=True,
        help_text='Year field.'
    )

    month = models.IntegerField(
        null=True,
        help_text='Month field'
    )

    class Meta:
        """
        Override the name.
        """

        verbose_name_plural = 'Histories'

    def __str__(self):
        """
        Returns history string.
        """

        return 'Username: {}, Service: {}, Type: {}'.format(
            self.user.username,
            self.service,
            self.types
        )
