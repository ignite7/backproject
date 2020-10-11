"""
Urlpatterns services.
"""

# Django
from django.urls import path

# Views
from ui.views import main_views, auth_views, service_views


urlpatterns = [
    # Main
    path(
        route='',
        view=main_views.IndexView.as_view(),
        name='index'
    ),

    path(
        route='releases/',
        view=main_views.ReleasesView.as_view(),
        name='releases'
    ),

    path(
        route='documentation/',
        view=main_views.DocumetationView.as_view(),
        name='documentation'
    ),

    path(
        route='contact/',
        view=main_views.ContactView.as_view(),
        name='contact'
    ),

    # Authentication
    path(
        route='login/',
        view=auth_views.LoginView,
        name='login'
    ),

    path(
        route='signup/',
        view=auth_views.SignupView,
        name='signup'
    ),

    path(
        route='logout/',
        view=auth_views.LogoutView,
        name='logout'
    ),

    path(
        route='email-confirmation/<str:key>/<str:secret>/',
        view=auth_views.EmailConfirmationView,
        name='email_confirmation'
    ),

    path(
        route='reset-password/',
        view=auth_views.ResetPasswordView,
        name='reset_password'
    ),

    path(
        route='reset-password/<str:key>/<str:secret>/',
        view=auth_views.ResetPasswordConfirmationView.as_view(),
        name='reset_password_confirmation'
    ),

    path(
        route='account/',
        view=auth_views.AccountView.as_view(),
        name='account'
    ),

    # Services
    path(
        route='history/',
        view=service_views.HistoryView.as_view(),
        name='history'
    ),

    path(
        route='favorites/',
        view=service_views.FavoriteView.as_view(),
        name='favorites'
    ),

    path(
        route='results/<str:service>/<slug:uuid>/',
        view=service_views.ResultView.as_view(),
        name='results'
    )
]
