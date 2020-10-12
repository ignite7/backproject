"""
Main forms UI.
"""

# Django REST framework
from rest_framework import status

# Django
from django import forms
from django.core.validators import RegexValidator, validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages

# Models
from models.models import Histories, Favorites
from back.settings import HOST

# Tasks
from ui.tasks.main_tasks import send_contact_email

# Crispy libraries
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

# Utilities
from requests import post


class HistoriesModelForm(forms.ModelForm):
    """
    Histories model form.
    """

    def clean(self):
        """
        Validate fields.
        """

        data = super().clean()
        return data

    class Meta:
        """
        Fields of the model `Histories`.
        """

        model = Histories
        fields = (
            'service',
            'types',
            'search'
        )


class IndexForm(HistoriesModelForm):
    """
    Index form.
    """

    pass


class ReleasesForm(HistoriesModelForm):
    """
    Releases form.
    """

    search = forms.CharField(required=False)
    month = forms.CharField(required=False)

    class Meta(HistoriesModelForm.Meta):
        """
        Override meta class.
        """

        fields = (
            'service',
            'types',
            'search',
            'year',
            'month'
        )


class FavoriteForm(forms.ModelForm):
    """
    Favorite form.
    """

    form_type = forms.CharField()

    class Meta:
        """
        Fields of `Favorites` model.
        """

        model = Favorites
        fields = (
            'types',
            'uuid',
            'title',
            'release_date',
            'duration',
            'description',
            'rating',
            'image_cover'
        )

    def create_favorite(self, request):
        """
        Create a favorite item.
        """

        data = self.data
        url = '{}/services/favorites/{}/'.format(HOST, data['uuid'])
        headers = {
            'Accept': 'application/json; version=v1',
            'Authorization': request.session['token']['Authorization'],
            'Secret': request.session['token']['Secret']
        }
        response = post(url, data=data, headers=headers)

        if response.status_code != status.HTTP_201_CREATED:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'Added to your favorites @{}'.format(
            request.user.username
        ))


class ContactForm(forms.Form):
    """
    Contact form
    """

    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Name'}),
        min_length=1,
        max_length=30
    )

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        min_length=3,
        max_length=254
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message=('Format: +9 99999999 Up to 15 digits allowed.')
    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Phone'}),
        validators=[phone_regex],
        min_length=1,
        max_length=15
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Subject'}),
        max_length=30
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Message'})
    )

    def __init__(self, *args, **kwargs):
        """
        Crispy form.
        """

        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='for-row'
            ),
            Row(
                Column('subject', css_class='form-group col-md-6'),
                Column('phone', css_class='form-group col-md-6'),
                css_class='for-row'
            ),
            Row(
                Column('message', css_class='form-group')
            ),
            Row(
                Submit('submit', 'Send', css_class='btn btn-success btn-block')
            )
        )

    def clean(self):
        """
        Validate email.
        """

        data = super().clean()

        try:
            validate_email(data['email'])

        except (ValidationError, KeyError):
            raise forms.ValidationError('Invalid email.')

        return data

    def send_email(self):
        """
        Send email if everything is rigth.
        """

        send_contact_email.delay(self.cleaned_data)
