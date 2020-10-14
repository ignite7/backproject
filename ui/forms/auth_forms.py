"""
Auth forms UI.
"""

# Django REST framework
from rest_framework import status

# Django
from django import forms
from django.core.validators import RegexValidator, validate_email
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib import messages

# Models
from models.models import Users, Tokens

# Modules
from api.auths.utils import login_user
from back.settings import REAL_HOST

# Crispy libraries
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Hidden
from crispy_forms.bootstrap import PrependedText

# Utilities
from requests import post, put, patch, delete


class SignupForm(forms.Form):
    """
    signup form.
    """

    email = forms.CharField(
        widget=forms.EmailInput(),
        min_length=3,
        max_length=254
    )

    username = forms.CharField(
        widget=forms.TextInput(),
        validators=[UnicodeUsernameValidator()],
        max_length=25
    )

    first_name = forms.CharField(
        min_length=2,
        max_length=150,
        required=False
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=150,
        required=False
    )

    picture = forms.ImageField(required=False)

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Format: +9 99999999 Up to 15 digits allowed.')
    )

    phone = forms.CharField(
        max_length=15,
        required=False,
        validators=[phone_regex]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=12
    )

    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=12
    )

    def clean(self):
        """
        Validate data.
        """

        data = super().clean()

        if data['password'] != data['password_confirmation']:
            raise forms.ValidationError('Passwords did not match.')

        if Users.objects.filter(email=data['email']).exists():
            raise forms.ValidationError('Email is already in use.')

        if Users.objects.filter(username=data['username']).exists():
            raise forms.ValidationError('Username is already in use.')

        if not data['picture']:
            data.pop('picture')

        try:
            validate_email(data['email'])
            password_validation.validate_password(data['password'])

        except (ValidationError, KeyError):
            raise forms.ValidationError('Invalid email or password')

        return data

    def create_user(self, request):
        """
        Authenticate user.
        """

        data = self.cleaned_data
        url = '{}/auth/signup/'.format(REAL_HOST)
        headers = {'Accept': 'application/json; version=v1'}
        response = post(url, data=data, headers=headers)

        if response.status_code != status.HTTP_201_CREATED:
            return messages.error(request, 'Something was wrong.')

        return messages.success(
            request, 'Welcome @{}, you have 24h for confirm your email.'.format(data['username'])
        )


class LoginForm(forms.Form):
    """
    Login form.
    """

    email = forms.CharField(
        widget=forms.EmailInput(),
        min_length=3,
        max_length=254
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=12
    )

    def clean(self):
        """
        Validate data.
        """

        data = super().clean()

        try:
            validate_email(data['email'])
            password_validation.validate_password(data['password'])

        except (ValidationError, KeyError):
            raise forms.ValidationError('Invalid email or password')

        return data

    def authenticate_user(self, request):
        """
        Authenticate user.
        """

        auth = login_user(self.cleaned_data, request)

        if not auth:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'You are logged in now @{}.'.format(
            auth['user'].username
        ))


class ResetPasswordForm(forms.Form):
    """
    Reset password form.
    """

    username = forms.CharField(
        widget=forms.TextInput(),
        validators=[UnicodeUsernameValidator()],
        min_length=4,
        max_length=25
    )

    email = forms.CharField(
        widget=forms.EmailInput(),
        min_length=3,
        max_length=254
    )

    email_confirmation = forms.CharField(
        widget=forms.EmailInput(),
        min_length=3,
        max_length=254
    )

    def clean(self):
        """
        Validate data.
        """

        data = super().clean()

        if data['email'] != data['email_confirmation']:
            raise forms.ValidationError('Emails did not match.')

        user = Users.objects.filter(username=data['username'])

        if not user.exists():
            raise forms.ValidationError('Username not exists.')

        for info_user in user:
            if Tokens.objects.filter(user=info_user, mode=3).exists():
                raise forms.ValidationError('Reset password has already been requested.')

            if info_user.email != data['email']:
                raise forms.ValidationError('Incorrect email.')

        return data

    def send_reset_password_email(self, request):
        """
        Send the reset password email to
        the user.
        """

        data = self.cleaned_data
        url = '{}/auth/reset-password/'.format(REAL_HOST)
        headers = {'Accept': 'application/json; version=v1'}
        response = post(url, data=data, headers=headers)

        if response.status_code != status.HTTP_201_CREATED:
            return messages.error(request, 'Something was wrong.')

        return messages.success(
            request,
            'Hello @{}, you will recive an email for reset your password before 3h'.format(
                data['username']
            )
        )


class ResetPasswordConfirmationForm(forms.Form):
    """
    Reset password confirmation form.
    """

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
        min_length=12
    )

    new_password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New password confirmation'}),
        min_length=12
    )

    def __init__(self, *args, **kwargs):
        """
        Crispy form.
        """

        super(ResetPasswordConfirmationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('new_password', css_class='form-group')
            ),
            Row(
                Column('new_password_confirmation', css_class='form-group')
            ),
            Row(
                Submit('submit', 'Reset Password', css_class='btn btn-success btn-block')
            )
        )

    def clean(self):
        """
        Validate data.
        """

        data = super().clean()

        if data['new_password'] != data['new_password_confirmation']:
            raise forms.ValidationError('New passwords did not match.')

        return data

    def reset_password(self, request, **kwargs):
        """
        Reset the user password.
        """

        url = '{}/auth/reset-password/{}/{}/'.format(REAL_HOST, kwargs['key'], kwargs['secret'])
        headers = {'Accept': 'application/json; version=v1'}
        response = put(url, data=self.cleaned_data, headers=headers)

        if response.status_code != status.HTTP_200_OK:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'The password has been changed successfully.')


class EmailConfirmationForm(forms.Form):
    """
    Email confirmation form.
    """

    def clean(self):
        """
        Validate keys.
        """

        data = super().clean()

        return data

    def activate_email(self, request, **kwargs):
        """
        Activate user email.
        """

        url = '{}/auth/email-confirmation/{}/{}/'.format(REAL_HOST, kwargs['key'], kwargs['secret'])
        headers = {'Accept': 'application/json; version=v1'}
        response = put(url, headers=headers)

        if response.status_code != status.HTTP_202_ACCEPTED:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'Your email has been confirmed.')


class AccountUpdateForm(forms.Form):
    """
    Account form.
    """

    authorization = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Authorization key'})
    )

    secret = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Secret key'})
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        min_length=3,
        max_length=254,
        required=False
    )

    email_confirmation = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email confirmation'}),
        min_length=3,
        max_length=254,
        required=False
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        validators=[UnicodeUsernameValidator()],
        max_length=25,
        required=False
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First name'}),
        min_length=2,
        max_length=150,
        required=False
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}),
        min_length=2,
        max_length=150,
        required=False
    )

    picture = forms.ImageField(required=False)

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Format: +9 99999999 Up to 15 digits allowed.')
    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Phone'}),
        max_length=15,
        required=False,
        validators=[phone_regex]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        min_length=12,
        required=False
    )

    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}),
        min_length=12,
        required=False
    )

    form_type = forms.CharField()

    def __init__(self, *args, **kwargs):
        """
        Crispy form.
        """

        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column(
                    PrependedText('authorization', 'Authorization key'),
                    css_class='form-group col-md-6'
                ),
                Column(
                    PrependedText('secret', 'Secret key'),
                    css_class='form-group col-md-6'
                ),
            ),
            Row(
                Column('email', css_class='form-group col-md-6'),
                Column('email_confirmation', css_class='form-group col-md-6'),
                css_class='for-row'
            ),
            Row(
                Column(PrependedText('username', '@'), css_class='form-group'),
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                css_class='for-row'
            ),
            Row(
                Column('phone', css_class='form-group col-md-6'),
                Column('picture', css_class='form-group col-md-6'),
                css_class='for-row'
            ),
            Row(
                Column('password', css_class='form-group col-md-6'),
                Column('password_confirmation', css_class='form-group col-md-6'),
                css_class='for-row'
            ),
            Row(
                Column(Hidden('form_type', 'update_user'), css_class='form-group')
            ),
            Row(
                Submit('submit', 'Update Profile', css_class='btn btn-success btn-block')
            )
        )

    def clean(self):
        """
        Validate data.
        """

        data = super().clean()

        if data['email'] and not data['email_confirmation']:
            raise forms.ValidationError('Fill out email confirmation field.')

        if data['password'] and not data['password_confirmation']:
            raise forms.ValidationError('Fill out password confirmation field.')

        if Users.objects.filter(email=data['email']).exists():
            raise forms.ValidationError('Email already exists.')

        if Users.objects.filter(username=data['username']).exists():
            raise forms.ValidationError('Username already exists.')

        if not data['picture']:
            data.pop('picture')

        if data['email']:
            try:
                validate_email(data['email'])
            except (ValidationError, KeyError):
                raise forms.ValidationError('Invalid email.')

        if data['password']:
            try:
                password_validation.validate_password(data['password'])
            except (ValidationError, KeyError):
                raise forms.ValidationError('Invalid password.')

        return data

    def update_user(self, request):
        """
        Update user.
        """

        url = '{}/auth/account/'.format(REAL_HOST)
        headers = {
            'Accept': 'application/json; version=v1',
            'Authorization': request.session['token']['Authorization'],
            'Secret': request.session['token']['Secret']
        }
        response = patch(url, data=self.cleaned_data, headers=headers)

        if response.status_code != status.HTTP_200_OK:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'Your profile @{} has been updated.'.format(
            request.user.username
        ))


class AccountDeleteForm(forms.Form):
    """
    Account delete form.
    """

    authorization = forms.CharField(
        widget=forms.PasswordInput()
    )

    secret = forms.CharField(
        widget=forms.PasswordInput()
    )

    form_type = forms.CharField()

    def clean(self):
        """
        Clean data.
        """

        data = super().clean()

        return data

    def delete_user(self, request):
        """
        Delete user.
        """

        url = '{}/auth/account/'.format(REAL_HOST)
        headers = {
            'Accept': 'application/json; version=v1',
            'Authorization': request.session['token']['Authorization'],
            'Secret': request.session['token']['Secret']
        }
        response = delete(url, data=self.cleaned_data, headers=headers)

        if response.status_code != status.HTTP_204_NO_CONTENT:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'Your profile has been deleted.')
