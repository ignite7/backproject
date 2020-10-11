"""
Services test endpoints.
"""

# Django
from django.urls import reverse

# Django REST framework
from rest_framework import status
from rest_framework.test import APITestCase

# Models
from models.models import Users


class EndpointsTestCase(APITestCase):
    """
    Testing endpoints.
    """

    def setUp(self):
        """
        Init test.
        """

        self.user = Users.objects.create_user(
            username='example',
            email='example@good.com',
            password='Sure123456789!',
            verified_email=True

        )

        # Provide credentials
        url = reverse('auth:login')
        data = {'email': self.user.email, 'password': 'Sure123456789!'}
        response = self.client.post(url, data, format='json')
        self.headers = {
            'Authorization': response.data['token']['Authorization'],
            'Secret': response.data['token']['Secret'],
            'Accept': 'application/json; version=v1'
        }

    def test_movieseries(self):
        """
        Movieseries endpoint.
        """

        # Filter by uuid
        url = reverse('services:movieseries', kwargs={'uuid': 'tt0077031'})
        data = {'service': 'movieseries', 'types': 'uuid'}
        response = self.client.get(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # Filter by search all
        url = reverse('services:search')
        data = {
            'service': 'movieseries',
            'types': 'search_all',
            'search': 'avengers'
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # Filter by data
        url = reverse('services:releases')
        data = {
            'service': 'movieseries',
            'types': 'date',
            'year': '2019'
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_games(self):
        """
        Games endpoint.
        """

        # Filter by uuid
        url = reverse('services:games', kwargs={'uuid': '500'})
        data = {'service': 'games', 'types': 'uuid'}
        response = self.client.get(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # Filter by search all
        url = reverse('services:search')
        data = {
            'service': 'games',
            'types': 'search_all',
            'search': 'GTA V'
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # Filter by data
        url = reverse('services:releases')
        data = {
            'service': 'games',
            'types': 'date',
            'search': 'PC',
            'year': '2019',
            'month': '07'
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_music(self):
        """
        Music endpoint.
        """

        # Filter by uuid
        url = reverse('services:music', kwargs={'uuid': '36QJpDe2go2KgaRleHCDTp'})
        data = {'service': 'music', 'types': 'uuid'}
        response = self.client.get(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # Filter by search all
        url = reverse('services:search')
        data = {
            'service': 'music',
            'types': 'search_all',
            'search': 'Beatles'
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # Filter by data
        url = reverse('services:releases')
        data = {
            'service': 'music',
            'types': 'date',
            'year': '2019',
            'month': '05'
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_coming_soon(self):
        """
        Comin soon endpoint.
        """

        url = reverse('services:releases')
        data = {'service': 'all', 'types': 'coming_soon'}
        response = self.client.get(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_history(self):
        """
        History endpoint.
        """

        # Retrieve history
        url = reverse('services:history_list_or_create_or_delete_all')
        response = self.client.get(url, {}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # Create history
        data = {
            "service": "music",
            "types": "search_all",
            "search": "Good daddy",
            "year": 2019,
            "month": 8
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data)

        # Delete history
        url = reverse('services:history_delete', kwargs={'uuid': 1})
        response = self.client.delete(url, {}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)

    def test_favorite(self):
        """
        Favorite endpoint.
        """

        # Retrieve favorite
        url = reverse('services:favorite_list_or_delete_all')
        response = self.client.get(url, {}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # Create favorite
        url = reverse('services:favorite_create_or_delete', kwargs={'uuid': 'HSADnddsw2'})
        data = {
            "title": "Hulk",
            "release_date": "07/07/2000",
            "duration": "1h",
            "description": "It's very good",
            "rating": 8.5,
            "image_cover": "HSdujer3k38"
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data)

        # Delete favorite
        response = self.client.delete(url, {}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
