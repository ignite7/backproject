"""
Services test models.
"""

# Django
from django.test import TestCase

# Models
from models.models import Users, Histories, Favorites


class ModelsTestCase(TestCase):
    """
    Model testing.
    """

    def setUp(self):
        """
        Init test.
        """

        user = Users.objects.create_user(
            username='example',
            email='example@good.com',
            password='Sure123456789!'
        )
        self.user = Users.objects.get(pk=user.pk)
        self.assertIsNotNone(self.user)

    def test_create_history(self):
        """
        Create history.
        """

        history = Histories.objects.create(
            user=self.user,
            service='games',
            types='search_all',
            search='GTA V',
            year=2015,
            month=7
        )
        self.assertTrue(history)

    def test_create_favorite(self):
        """
        Create favorite.
        """

        favorite = Favorites.objects.create(
            user=self.user,
            types='games',
            uuid='452',
            title='GTA V',
            release_date='2015-07',
            duration='8 hours',
            description='Long description...',
            rating=9.5,
            image_cover='thisisthecover'
        )
        self.assertTrue(favorite)
