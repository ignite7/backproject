"""
Urlpatterns auths.
"""

# Django
from django.urls import path

# Views
from api.auths import views


urlpatterns = [
    path(
        route='login/',
        view=views.LoginView.as_view(),
        name='login'
    ),

    path(
        route='signup/',
        view=views.SignupView.as_view(),
        name='signup'
    ),

    path(
        route='logout/',
        view=views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        route='email-confirmation/<str:key>/<str:secret>/',
        view=views.ConfirmEmailView.as_view(),
        name='email_confirmation'
    ),

    path(
        route='reset-password/',
        view=views.ResetPasswordView.as_view({'post': 'create'}),
        name='reset_password_create'
    ),

    path(
        route='reset-password/<str:key>/<str:secret>/',
        view=views.ResetPasswordView.as_view({'put': 'update'}),
        name='reset_password_update'
    ),

    path(
        route='account/',
        view=views.AccountView.as_view(),
        name='account'
    )
]
