"""
Serializers services.
"""

# Django REST Framework
from rest_framework import serializers, exceptions, status
from rest_framework.validators import UniqueValidator

# Django
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email

# Models
from models.models import Users, RegexValidator, Tokens

# Modules
from api.auths.utils import (
    get_authentication,
    create_token,
    decode_token,
    delete_token,
    login_user,
    logout_user
)

# Tasks
from api.auths.tasks import send_email_confirmation, send_reset_password


class UserModelSerializer(serializers.ModelSerializer):
    """
    User model serializer.
    """

    class Meta:
        """
        Model and field that it
        gonna be used.
        """

        model = Users
        fields = (
            'email',
            'username',
            'is_verified',
            'first_name',
            'last_name',
            'phone',
            'picture'
        )


class SignupSerializer(serializers.Serializer):
    """
    Validate the signup data.
    """

    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=Users.objects.all())],
        label='Email',
        help_text='Email field.'
    )

    username = serializers.CharField(
        min_length=4,
        max_length=25,
        validators=[
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=Users.objects.all())
        ],
        label='Username',
        help_text='Username field.'
    )

    first_name = serializers.CharField(
        min_length=2,
        max_length=150,
        required=False,
        label='First name',
        help_text='First name filed.'
    )

    last_name = serializers.CharField(
        min_length=2,
        max_length=150,
        required=False,
        label='Last name',
        help_text='Last name filed.'
    )

    picture = serializers.ImageField(
        required=False,
        label='Picture',
        help_text='Picture field.'
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Format: +9 99999999 Up to 15 digits allowed.')
    )

    phone = serializers.CharField(
        max_length=15,
        required=False,
        validators=[phone_regex],
        label='Phone',
        help_text='Phone field'
    )

    password = serializers.CharField(
        min_length=12,
        label='Password',
        help_text='Password field.'
    )

    password_confirmation = serializers.CharField(
        min_length=12,
        label='Password confirmation',
        help_text='Password confirmation field.'
    )

    def validate(self, data):
        """
        Validate is the passwords is matched.
        """

        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Passwords did not match.')

        validate_email(data['email'])
        password_validation.validate_password(data['password'])
        self.context['data'] = data

        return data

    def create(self):
        """
        Create the user.
        """

        data = self.context['data']

        user = Users.objects.create_user(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            picture=data.get('picture'),
            phone=data.get('phone'),
            is_verified=False,
            verified_email=False
        )

        send_email_confirmation.delay(
            UserModelSerializer(user).data,
            create_token(data['username'], 2, self.context['request'])
        )

        return {
            'user': UserModelSerializer(user).data,
            'verification': 'Confirm your email in 24h.'
        }


class LoginSerializer(serializers.Serializer):
    """
    Validate the login data.
    """

    email = serializers.EmailField(
        max_length=254,
        label='Email',
        help_text='Email field.'
    )

    password = serializers.CharField(
        min_length=12,
        label='Password',
        help_text='Password field.'
    )

    def validate(self, data):
        """
        Check the user credentials.
        """

        if self.context['request'].user.is_authenticated:
            raise serializers.ValidationError('Already logged in')

        validate_email(data['email'])
        password_validation.validate_password(data['password'])

        self.context['data'] = data

        return data

    def create(self):
        """
        Generate a new token every time the
        user logged in.
        """

        request = self.context['request']
        data = self.context['data']
        auth = login_user(data, request)

        if not auth:
            raise exceptions.AuthenticationFailed(status.HTTP_401_UNAUTHORIZED)

        return {
            'user': UserModelSerializer(auth['user']).data,
            'token': auth['token']
        }


class LogoutSerializer(serializers.Serializer):
    """
    Validate the data.
    """

    def destroy(self):
        """
        Delete the token of the
        user.
        """

        request = self.context['request']
        logout_user(request.user.username, 1, request)


class ConfirmEmailSerializer(serializers.Serializer):
    """
    Validate the data.
    """

    def update(self):
        """
        Validate the token.
        """

        data = self.context['kwargs']

        try:
            token = decode_token(data['key'], data['secret'], 2)
            user = Users.objects.get(username=token['username'])

            if user.verified_email:
                raise serializers.ValidationError('User is already verified.')

            if token['mode'] != 2:
                raise serializers.ValidationError('Token not related.')

            self.context['user'] = user
            self.save()

        except Users.DoesNotExist:
            raise serializers.ValidationError('User not exists.')

    def save(self):
        """
        Change user to verified email
        and delete the token.
        """

        delete_token(self.context['user'].username, 2)
        self.context['user'].verified_email = True
        self.context['user'].save()


class ResetPasswordSerializer(serializers.Serializer):
    """
    Reset password serializer.
    """

    username = serializers.CharField(
        min_length=4,
        max_length=15,
        validators=[UnicodeUsernameValidator()],
        label='Username',
        help_text='Username field.'
    )

    email = serializers.EmailField(
        max_length=254,
        label='Email',
        help_text='Email field.'
    )

    email_confirmation = serializers.EmailField(
        max_length=254,
        label='Email confirmation',
        help_text='Email field.'
    )

    def validate(self, data):
        """
        Validate the token.
        """

        request = self.context['request']
        user = Users.objects.filter(username=data['username'])

        if request.user.is_authenticated:
            raise serializers.ValidationError('You are logged in.')

        if data['email'] != data['email_confirmation']:
            raise serializers.ValidationError('Emails did not match.')

        if not user.exists():
            raise serializers.ValidationError('Username not exists.')

        for info_user in user:
            if Tokens.objects.filter(user=info_user, mode=3).exists():
                raise serializers.ValidationError('Reset password has already been requested.')

            if info_user.email != data['email']:
                raise serializers.ValidationError('Incorrect email.')

        validate_email(data['email'])
        self.context['username'] = data['username']

        return data

    def create(self):
        send_reset_password.delay(
            self.context['username'],
            create_token(self.context['username'], 3, self.context['request'])
        )


class ResetPasswordUpdateSerializer(serializers.Serializer):
    """
    Reset password update serializer.
    """

    new_password = serializers.CharField(
        min_length=12,
        label='Password',
        help_text='Password field.'
    )

    new_password_confirmation = serializers.CharField(
        min_length=12,
        label='Password confirmation',
        help_text='Password confirmation field.'
    )

    def validate(self, data):
        """
        Validate passwords are equals and
        validate token passed.
        """

        request = self.context['request']

        if request.user.is_authenticated:
            raise serializers.ValidationError('You are logged in.')

        if data['new_password'] != data['new_password_confirmation']:
            raise serializers.ValidationError('Passwords did not match.')

        password_validation.validate_password(data['new_password'])

        try:
            slug = self.context['kwargs']
            token = decode_token(slug['key'], slug['secret'], 3)
            user = Users.objects.get(username=token['username'])

            if token['mode'] != 3:
                raise serializers.ValidationError('Token not related.')

            self.context.update({'user': user, 'passwd': data['new_password']})

            return data

        except Users.DoesNotExist:
            raise serializers.ValidationError('User not exists.')

    def update(self):
        """
        Update the password of the user.
        """

        delete_token(self.context['user'].username, 3)
        self.context['user'].password = make_password(self.context['passwd'])
        self.context['user'].save()


class AccountSerializer(serializers.Serializer):
    """
    Account serializer.
    """

    authorization = serializers.CharField(
        min_length=25,
        label='Authorization',
        help_text='Authorization field'
    )

    secret = serializers.CharField(
        min_length=25,
        label='Secret',
        help_text='Secret field'
    )

    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=Users.objects.all())],
        required=False,
        label='Email',
        help_text='Email field.'
    )

    email_confirmation = serializers.EmailField(
        max_length=254,
        required=False,
        label='Email confirmation',
        help_text='Email field.'
    )

    username = serializers.CharField(
        min_length=4,
        max_length=15,
        validators=[
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=Users.objects.all())
        ],
        required=False,
        label='Username',
        help_text='Username field.'
    )

    first_name = serializers.CharField(
        min_length=2,
        max_length=50,
        required=False,
        label='First name',
        help_text='First name filed.'
    )

    last_name = serializers.CharField(
        min_length=2,
        max_length=50,
        required=False,
        label='Last name',
        help_text='Last name filed.'
    )

    picture = serializers.ImageField(
        required=False,
        label='Picture',
        help_text='Picture field.'
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Format: +9 99999999 Up to 15 digits allowed.')
    )

    phone = serializers.CharField(
        max_length=15,
        required=False,
        validators=[phone_regex],
        label='Phone',
        help_text='Phone field'
    )

    password = serializers.CharField(
        min_length=12,
        label='Password',
        required=False,
        help_text='Password field.'
    )

    password_confirmation = serializers.CharField(
        min_length=12,
        required=False,
        label='Password confirmation',
        help_text='Password confirmation field.'
    )

    def validate(self, data):
        """
        Validate emails and passwords are
        equally, confirmations are filled
        out in case the user wants to change
        the email or password and token
        it's okay.
        """

        request = self.context['request']
        token = decode_token(data['authorization'], data['secret'], 1)
        user = Users.objects.get(username=token['username'])

        if data.get('email'):
            if not data.get('email_confirmation'):
                raise serializers.ValidationError(
                    'Fill out the email confirmation field.'
                )
            elif data.get('email') != data.get('email_confirmation'):
                raise serializers.ValidationError(
                    'Emails did not match.'
                )

            validate_email(data['email'])
            user.email = data['email']
            user.verified_email = False
            send_email_confirmation.delay(
                UserModelSerializer(user).data,
                create_token(user.username, 2, request)
            )
            logout_user(user.username, 1, request)

        elif data.get('password'):
            if not data.get('password_confirmation'):
                raise serializers.ValidationError(
                    'Fill out password confirmation field.'
                )
            elif data.get('password') != data.get('password_confirmation'):
                raise serializers.ValidationError(
                    'Passwords did not match.'
                )

            password_validation.validate_password(data['password'])
            user.password = make_password(data['password'])
            logout_user(user.username, 1, request)

        self.context['user'] = user
        self.context['token'] = token
        self.context['data'] = data

        return data

    def update(self):
        """
        Update the user fields.
        """

        user = self.context['user']
        data = self.context['data']

        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone = data.get('phone', user.phone)
        user.picture = data.get('picture', user.picture)

        self.context['user'] = user

    def save(self, **kwargs):
        """
        Save the user instance.
        """

        self.update()
        user = self.context['user']
        user.save()

        return {'user': UserModelSerializer(user).data}


class AccountDeleteSerializer(AccountSerializer):
    """
    Account delete serializer.
    """

    def validate(self, data):
        """
        Validate token.
        """

        token = decode_token(data['authorization'], data['secret'], 1)
        self.context['token'] = token

        return data

    def destroy(self):
        """
        Delete the user account.
        """

        delete_token(self.context['token']['username'], 1)
        Users.objects.get(
            username=self.context['token']['username']
        ).delete()


class AccountNotRequiredSerializer(AccountSerializer):
    """
    Account not required serializer.
    """

    authorization = serializers.CharField(required=False)
    secret = serializers.CharField(required=False)
    picture = serializers.CharField(required=False)

    def validate(self, data):
        """
        Validate authentication of the
        user.
        """

        request = self.context['request']
        user = get_authentication(request)
        data = UserModelSerializer(user).data

        try:
            data['authorization'] = request.session['token']['Authorization']
            data['secret'] = request.session['token']['Secret']

        except (KeyError, TypeError):
            serializers.ValidationError('Not authorized.')

        return data
