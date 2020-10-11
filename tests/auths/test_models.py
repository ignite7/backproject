"""
Auths test models.
"""

# Django
from django.test import TestCase

# Models
from models.models import Users, Tokens, Restricts


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

    def test_tokens(self):
        """
        Create token.
        """

        token = Tokens.objects.create(
            user=self.user,
            key='This is a long unsecure key',
            secret='This is a lon unsecure secret',
            mode=1
        )
        self.assertIsNotNone(token)

    def test_retricts(self):
        """
        Create restric.
        """

        ip_addr = Restricts.objects.create(
            ip_remote_addr='192.168.92.10',
            requests=2
        )
        self.assertIsNotNone(ip_addr)
