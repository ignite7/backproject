"""
Model favorites.
"""

# Models
from models.models import models, Commons, Users


class Favorites(Commons):
    """
    This class it's gonna handle to
    save the favorite games of the
    user.
    """

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        help_text='Users info.'
    )

    types = models.CharField(
        max_length=25,
        help_text='Type.'
    )

    uuid = models.CharField(
        max_length=50,
        unique=True,
        help_text='UUID Movie or Serie.'
    )

    title = models.CharField(
        max_length=250,
        help_text='Title.'
    )

    release_date = models.CharField(
        max_length=25,
        help_text='Release date.'
    )

    duration = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        help_text='Time to beat.'
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text='Summary.'
    )

    rating = models.FloatField(
        null=True,
        help_text='Raiting.'
    )

    image_cover = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text='Image Cover.'
    )

    class Meta:
        """
        Override the name.
        """

        verbose_name_plural = 'Favorites'

    def __str__(self):
        """
        Returns favorite string.
        """

        return 'Username: {}, uuid: {}, Title: {}'.format(
            self.user.username,
            self.uuid,
            self.title
        )
