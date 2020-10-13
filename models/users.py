"""
Models auths.
"""

# Django REST framework
from rest_framework import exceptions
from rest_framework.authentication import (
    TokenAuthentication,
    get_authorization_header
)

# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Models
from models.models import models, Commons

# PyJWT
import jwt


class Users(Commons, AbstractUser):
    """
    This class it will be handle to
    implement the auth to the user.
    """

    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True,
        help_text='Email is unique.'
    )

    username = models.CharField(
        'username',
        max_length=25,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        help_text='Username field.'
    )

    password = models.TextField(
        name='password',
        help_text='Password field.'
    )

    picture = models.ImageField(
        upload_to='media/pictures/users/',
        blank=True,
        null=True,
        help_text='Picture of the user.'
    )

    verified_email = models.BooleanField(
        default=False,
        help_text='Email confirmation.'
    )

    is_verified = models.BooleanField(
        default=False,
        help_text='Verified user field.'
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Format: +9 99999999 Up to 15 digits allowed.')
    )

    phone = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        null=True,
        help_text='Phone of the user.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        """
        Override the name.
        """

        verbose_name_plural = 'Users'

    def __str__(self):
        """
        Returns username string.
        """

        return self.username

    def get_short_name(self):
        """
        Returns short name string.
        """

        return self.username

    def get_full_name(self):
        """
        Returns full name string.
        """

        return 'Username: {}, First Name: {}, Last Name: {}'.format(
            self.username,
            self.first_name,
            self.last_name
        )

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.
        """

        subject = 'Hello @{}, {} <Back.com>'.format(self.username, subject)
        content = render_to_string(
            'emails/EmailUser.html',
            {'message': message, 'kwargs': kwargs}
        )
        message = EmailMultiAlternatives(
            subject=subject,
            body=content,
            from_email=from_email,
            to=[self.email]
        )
        message.attach_alternative(content, "text/html")
        message.send()


class Tokens(Commons):
    """
    This class it gonna handle to
    save the token of the user.
    """

    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        help_text='Info users.'
    )

    mode = models.IntegerField(
        help_text=(
            'Indicates the mode of the token, modes:\n'
            '1- Main = 1h\n'
            '2- Email confirmation = 24h\n'
            '3- Reset password = 3h\n'
        )
    )

    key = models.TextField(
        unique=True,
        help_text='Key token.'
    )

    secret = models.TextField(
        unique=True,
        help_text='Provide a secret key to the user.'
    )

    class Meta:
        """
        Override the name.
        """

        verbose_name_plural = 'Tokens'

    def __str__(self):
        return 'Username: {}, Key: {}, Secret: {}, Token mode: {}'.format(
            self.user.username,
            self.key,
            self.secret,
            self.mode
        )


class TokensModel(TokenAuthentication):
    """
    This class is the token model
    of `Tokens`
    """

    model = Tokens
    mode = 1

    def authenticate(self, request):
        """
        Rewrite the authenticate function
        to allow read by hash key and not
        by raw key.
        """

        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(
                _('Invalid token or secret header. No credentials provided.')
            )

        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(_(
                'Invalid token or secret header. '
                'Token or secret string should not contain spaces.'
            ))

        try:
            payload = jwt.decode(
                jwt=auth[1].decode(),
                key=request.META['HTTP_SECRET'],
                algorithm='HS256'
            )

            if self.mode != payload['mode']:
                raise exceptions.AuthenticationFailed(_('Mode not allowed.'))

            token = self.model.objects.get(
                user=Users.objects.get(username=payload['username']),
                mode=payload['mode']
            )

            check_key = check_password(auth[1].decode(), token.key)
            check_secret = check_password(request.META['HTTP_SECRET'], token.secret)

            if not check_key or not check_secret:
                raise exceptions.AuthenticationFailed(
                    _('Invalid credentials.')
                )

        except (UnicodeError, KeyError, TypeError, self.model.DoesNotExist,
                Users.DoesNotExist):
            raise exceptions.AuthenticationFailed(_(
                'Invalid token or secret header. '
                'Token or secret string should not contain invalid characters.'
            ))

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(_('Token is out of date'))

        except jwt.exceptions.PyJWTError:
            raise exceptions.AuthenticationFailed(_('Invalid token or secret.'))

        return self.authenticate_credentials(token.key, token.secret)

    def authenticate_credentials(self, key, secret):
        """
        Override the `authenticate_credentials` to
        the model search by the `secret` and `mode`
        as well.
        """

        try:
            token = self.model.objects.select_related('user').get(
                key=key,
                secret=secret,
                mode=self.mode
            )

        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.')
            )

        return (token.user, token)


class Restricts(Commons):
    """
    Restrict the ip of the
    anonymous user.
    """

    ip_remote_addr = models.GenericIPAddressField(
        unique=True,
        help_text='Ip address.'
    )

    requests = models.PositiveIntegerField(
        help_text='Count the requests per hour by ip.'
    )

    class Meta:
        """
        Override the name.
        """

        verbose_name_plural = 'Retricts'

    def __str__(self):
        return 'IP remote address: {}, Request per day: {}'.format(
            self.ip_remote_addr,
            self.requests
        )
