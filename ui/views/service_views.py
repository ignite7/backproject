"""
Service views UI.
"""

# Django REST framework
from rest_framework import status

# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages

# Modules
from back import settings
from ui.utils import api

# Forms
from ui.forms.service_forms import (
    DeleteAllHistoryForm,
    DeleteHistoryForm,
    DeleteAllFavoriteForm,
    DeleteFavoriteForm
)
from ui.forms.main_forms import FavoriteForm

# Models
from models.models import Histories, Favorites


class HistoryView(LoginRequiredMixin, ListView):
    """
    History view.
    """

    http_method_names = ['get', 'post']
    template_name = 'ui/history.html'
    model = Histories
    context_object_name = 'histories'
    title = settings.TITLE + 'History'
    login_url = reverse_lazy('ui:index')
    ordering = ('-created_at')
    paginate_by = 12

    def get_queryset(self):
        """
        Get the current user.
        """

        queryset = Histories.objects.filter(
            user=self.request.user,
            is_used=True
        )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data.
        """

        context = super(HistoryView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        data = request.POST

        if data['form_type'] == 'delete_all':
            form = DeleteAllHistoryForm(data)

            if form.is_valid():
                form.delete_all_history(request)

        elif data['form_type'] == 'delete':
            form = DeleteHistoryForm(data)

            if form.is_valid():
                form.delete_history(request)

        return redirect('ui:history')


class FavoriteView(LoginRequiredMixin, ListView):
    """
    Favorite view
    """

    http_method_names = ['get', 'post']
    template_name = 'ui/favorite.html'
    model = Favorites
    context_object_name = 'favorites'
    title = settings.TITLE + 'My Favorites'
    login_url = reverse_lazy('ui:index')
    ordering = ('-created_at')
    paginate_by = 12

    def get_queryset(self):
        """
        Get the current user.
        """

        queryset = Favorites.objects.filter(
            user=self.request.user,
            is_used=True
        )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data.
        """

        context = super(FavoriteView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        data = request.POST

        if data['form_type'] == 'delete_all':
            form = DeleteAllFavoriteForm(data)

            if form.is_valid():
                form.delete_all_favorites(request)

        elif data['form_type'] == 'delete':
            form = DeleteFavoriteForm(data)

            if form.is_valid():
                form.delete_favorite(request)

        return redirect('ui:favorites')


class ResultView(TemplateView):
    """
    Detail view.
    """

    http_method_names = ['get', 'post']
    title = settings.TITLE + 'Results'

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data.
        """

        context = super(ResultView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context

    def get(self, request, *args, **kwargs):
        """
        GET request.
        """

        if not kwargs['service'] in ['movieseries', 'games', 'music']:
            messages.error(request, 'Wrong service in the url.')
            return redirect('ui:index')

        title = self.get_context_data()['title']
        kwargs['types'] = 'uuid'
        data = api(request, kwargs)

        if data.status_code != status.HTTP_200_OK:
            messages.error(request, 'Something was wrong.')
            return redirect('ui:index')

        return render(
            request,
            'ui/result.html',
            context={'title': title, 'data': data.json()}
        )

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        data = request.POST

        if data['form_type'] == 'create_favorite':
            form = FavoriteForm(data)
            form.create_favorite(request)

        return redirect('ui:index')
