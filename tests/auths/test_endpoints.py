"""
Auths test endpoints.
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

        # Login endpoint
        url = reverse('auth:login')
        data = {'email': self.user.email, 'password': 'Sure123456789!'}
        response = self.client.post(url, data, format='json')
        self.headers = {
            'Authorization': response.data['token']['Authorization'],
            'Secret': response.data['token']['Secret'],
            'Accept': 'application/json; version=v1'
        }
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNotNone(response.data)

    def test_signup(self):
        """
        Signup endpoint.
        """

        url = reverse('auth:signup')
        data = {
            "email": "eddy@ed.com",
            "password": "Sure123456789!",
            "password_confirmation": "Sure123456789!",
            "first_name": "eddy",
            "last_name": "ed",
            "username": "pepe"
        }
        response = self.client.post(url, data, format='json')
        self.credentials = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data)

    def test_confirm_email(self):
        """
        Confirm email endpoint.
        """

        key = self.credentials['token']['Authorization'].split()[1]
        secret = self.credentials['token']['Secret']
        url = reverse('auth:email_confirmation', kwargs={'key': key, 'secret': secret})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.data, status.HTTP_202_ACCEPTED)

    def test_reset_password(self):
        """
        Reset password endpoint.
        """

        # Request reset password
        url = reverse('auth:reset_password_retrive_or_create')
        data = {
            "username": self.user.username,
            "email": self.user.email,
            "email_confirmation": self.user.email
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data)

        # Reset password
        key = response.data['token']['Authorization'].split()[1]
        secret = response.data['token']['Secret']
        url = reverse('auth:reset_password_update', kwargs={'key': key, 'secret': secret})
        data = {
            "new_password": "Newpassword1234!",
            "new_password_confirmation": "Newpassword1234!"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_account(self):
        """
        Account endpoint.
        """

        # Retrieve user
        url = reverse('auth:account')
        response = self.client.get(url, {}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # User partial update
        data = {
            'authorization': self.headers['Authorization'],
            'secret': self.headers['Secret'],
            'first_name': 'nemo'
        }
        response = self.client.patch(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

        # Delete user
        data = {
            'authorization': self.headers['Authorization'],
            'secret': self.headers['Secret']
        }
        response = self.client.delete(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)

    def test_logout(self):
        """
        Loguot endpoint.
        """

        url = reverse('auth:logout')
        response = self.client.delete(url, {}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
