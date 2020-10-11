"""
Auth views UI.
"""

# Django
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

# Forms
from ui.forms.auth_forms import (
    LoginForm,
    SignupForm,
    EmailConfirmationForm,
    ResetPasswordForm,
    ResetPasswordConfirmationForm,
    AccountUpdateForm,
    AccountDeleteForm
)

# Modules
from back import settings
from api.auths.utils import logout_user

# Models
from models.models import Users


def SignupView(request):
    """
    Signup view.
    """

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():
            form.create_user(request)

    return redirect('ui:index')


def EmailConfirmationView(request, key, secret):
    """
    Email confirmation view.
    """

    if request.method == 'GET':
        form = EmailConfirmationForm(request.GET)

        if form.is_valid():
            form.activate_email(request, key=key, secret=secret)

    return redirect('ui:index')


def LoginView(request):
    """
    Login view
    """

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            form.authenticate_user(request)

    return redirect('ui:index')


def ResetPasswordView(request):
    """
    Reset password view.
    """

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            form.send_reset_password_email(request)

    return redirect('ui:index')


class ResetPasswordConfirmationView(FormView):
    """
    Reset password confirmation view.
    """

    http_method_names = ['get', 'post']
    template_name = 'ui/reset_password.html'
    form_class = ResetPasswordConfirmationForm
    success_url = reverse_lazy('ui:index')
    title = settings.TITLE + 'Reset Password'

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data.
        """

        context = super(ResetPasswordConfirmationView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context

    def form_valid(self, form, **kwargs):
        """
        Check if form is valid.
        """

        form.reset_password(
            self.request,
            key=self.kwargs['key'],
            secret=self.kwargs['secret']
        )

        return super(ResetPasswordConfirmationView, self).form_valid(form)


@login_required
def LogoutView(request):
    """
    Logout view
    """

    if request.method == 'GET':
        logout_user(request.user.username, 1, request)
        messages.success(request, 'You are logged out now, see you soon!')

    return redirect('ui:index')


class AccountView(LoginRequiredMixin, ListView):
    """
    Account view.
    """

    http_method_names = ['get', 'post']
    template_name = 'ui/account.html'
    model = Users
    context_object_name = 'users'
    title = settings.TITLE + 'Account'
    login_url = reverse_lazy('ui:index')

    def get_queryset(self):
        """
        Get the current user.
        """

        queryset = Users.objects.get(pk=self.request.user.pk)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Retrieve the context data.
        """

        context = super(AccountView, self).get_context_data(**kwargs)
        context['title'] = self.title
        context['form'] = AccountUpdateForm()

        return context

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        data = request.POST

        if data['form_type'] == 'update_user':
            form = AccountUpdateForm(data, request.FILES)

            if form.is_valid():
                form.update_user(request)

            return redirect('ui:account')

        elif data['form_type'] == 'delete_user':
            form = AccountDeleteForm(data)

            if form.is_valid():
                form.delete_user(request)

            return redirect('ui:index')
