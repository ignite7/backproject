"""
Service forms UI.
"""

# Django REST framework
from rest_framework import status

# Django
from django import forms
from django.contrib import messages

# Modules
from back.settings import REAL_HOST

# Utilities
from requests import delete


class DeleteAllHistoryForm(forms.Form):
    """
    Delete all history form.
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

    def delete_all_history(self, request):
        """
        Delete all history.
        """

        url = '{}/services/history/'.format(REAL_HOST)
        headers = {
            'Accept': 'application/json; version=v1',
            'Authorization': request.session['token']['Authorization'],
            'Secret': request.session['token']['Secret']
        }
        response = delete(url, data=self.cleaned_data, headers=headers)

        if response.status_code != status.HTTP_204_NO_CONTENT:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'All your history has been delete @{}.'.format(
            request.user.username
        ))


class DeleteHistoryForm(forms.Form):
    """
    Delete history form.
    """

    uuid = forms.CharField()
    form_type = forms.CharField()

    def clean(self):
        """
        Clean data.
        """

        data = super().clean()

        return data

    def delete_history(self, request):
        """
        Delete id history.
        """

        data = self.cleaned_data
        url = '{}/services/history/{}/'.format(REAL_HOST, data['uuid'])
        headers = {
            'Accept': 'application/json; version=v1',
            'Authorization': request.session['token']['Authorization'],
            'Secret': request.session['token']['Secret']
        }
        response = delete(url, headers=headers)

        if response.status_code != status.HTTP_204_NO_CONTENT:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'The history item has been delete @{}.'.format(
            request.user.username
        ))


class DeleteAllFavoriteForm(forms.Form):
    """
    Delete all favorite form.
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

    def delete_all_favorites(self, request):
        """
        Delete all favorites.
        """

        url = '{}/services/favorites/'.format(REAL_HOST)
        headers = {
            'Accept': 'application/json; version=v1',
            'Authorization': request.session['token']['Authorization'],
            'Secret': request.session['token']['Secret']
        }
        response = delete(url, data=self.cleaned_data, headers=headers)

        if response.status_code != status.HTTP_204_NO_CONTENT:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'All your favorites has been delete @{}.'.format(
            request.user.username
        ))


class DeleteFavoriteForm(forms.Form):
    """
    Delete favorite form.
    """

    uuid = forms.CharField()
    form_type = forms.CharField()

    def clean(self):
        """
        Clean data.
        """

        data = super().clean()

        return data

    def delete_favorite(self, request):
        """
        Delete id favorite.
        """

        data = self.cleaned_data
        url = '{}/services/favorites/{}/'.format(REAL_HOST, data['uuid'])
        headers = {
            'Accept': 'application/json; version=v1',
            'Authorization': request.session['token']['Authorization'],
            'Secret': request.session['token']['Secret']
        }
        response = delete(url, headers=headers)

        if response.status_code != status.HTTP_204_NO_CONTENT:
            return messages.error(request, 'Something was wrong.')

        return messages.success(request, 'The favorite item has been delete @{}.'.format(
            request.user.username
        ))
