"""
Main views UI.
"""

# Django
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages

# Forms
from ui.forms.main_forms import (
    IndexForm,
    ReleasesForm,
    ContactForm,
    FavoriteForm
)

# Modules
from back import settings
from ui.utils import api


class IndexView(TemplateView):
    """
    Index view.
    """

    http_method_names = ['get', 'post']
    template_name = 'ui/index.html'
    title = settings.TITLE + 'Home'

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data.
        """

        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        title = self.get_context_data()['title']
        data = request.POST

        if data['form_type'] == 'search_all':
            form = IndexForm(data)

            if form.is_valid():
                data = api(request, form.cleaned_data)

            return render(request, 'ui/index.html', context={'title': title, 'data': data})

        elif data['form_type'] == 'create_favorite':
            form = FavoriteForm(data)
            form.create_favorite(request)

            return redirect('ui:index')


class ReleasesView(TemplateView):
    """
    Releases view.
    """

    http_method_names = ['get', 'post']
    title = settings.TITLE + 'Releases'

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data.
        """

        context = super(ReleasesView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context

    def get(self, request, *args, **kwargs):
        """
        GET request.
        """

        if request.method == 'POST':
            data = request.POST

            if data['form_type'] == 'create_favorite':
                form = FavoriteForm(data)
                form.create_favorite(request)

                return redirect('ui:index')

        title = self.get_context_data()['title']
        data = {'types': 'coming_soon'}
        coming_soon = api(request, data)

        return render(
            request,
            'ui/releases.html',
            context={'title': title, 'coming_soon': coming_soon}
        )

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        title = self.get_context_data()['title']
        data = request.POST

        if data['form_type'] == 'search_date':
            form = ReleasesForm(data)

            if form.is_valid():
                data = api(request, form.cleaned_data)
                date = '{}-{}'.format(form.cleaned_data['year'], form.cleaned_data['month'])

            return render(
                request,
                'ui/releases.html',
                context={'title': title, 'data': data, 'date': date}
            )

        elif data['form_type'] == 'create_favorite':
            form = FavoriteForm(data)
            form.create_favorite(request)

            return redirect('ui:index')


class DocumetationView(TemplateView):
    """
    Documentation view
    """

    http_method_names = ['get']
    template_name = 'ui/documentation.html'
    title = settings.TITLE + 'Documentation'

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data.
        """

        context = super(DocumetationView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context


class ContactView(FormView):
    """
    Contact view.
    """

    http_method_names = ['get', 'post']
    template_name = 'ui/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('ui:contact')
    title = settings.TITLE + 'Contact'

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data.
        """

        context = super(ContactView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context

    def form_valid(self, form):
        """
        Check if form is valid.
        """

        form.send_email()
        messages.success(
            self.request,
            'Message send successfully {}, we\'ll contact you ASAP.'.format(
                form.cleaned_data['name'].split()[0]
            )
        )

        return super(ContactView, self).form_valid(form)
