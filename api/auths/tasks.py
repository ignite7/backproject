"""
Tasks auths.
"""

# Django REST framework
from rest_framework import status

# Django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import global_settings

# Celery
from celery import shared_task
from celery.decorators import periodic_task

# Models
from models.models import Tokens

# Modules
from api.services.commons import status_code

# Utilities
import datetime


@shared_task(max_retries=3)
def send_email_confirmation(user, token):
    """
    This function send a confirmation
    email when the user create an
    account.
    """

    subject = 'Hello @{}, activate your account in <Back.com>'.format(user['username'])
    content = render_to_string('emails/email_verification.html', {
        'user': user,
        'token': token,
        'host': global_settings.ALLOWED_HOSTS[0]
    })
    message = EmailMultiAlternatives(
        subject=subject,
        body=content,
        from_email='team@back.com',
        to=[user['email']]
    )
    message.attach_alternative(content, "text/html")
    message.send()

    return status_code(status=status.HTTP_200_OK)


@shared_task(max_retries=3)
def send_reset_password(email, token):
    """
    This function send a confirmation
    email when the user create an
    account.
    """

    subject = 'Hello {}, reset your password in <Back.com>'.format(email)
    content = render_to_string('emails/reset_password.html', {
        'email': email,
        'token': token,
        'host': global_settings.ALLOWED_HOSTS[0]
    })
    message = EmailMultiAlternatives(
        subject=subject,
        body=content,
        from_email='team@back.com',
        to=[email]
    )
    message.attach_alternative(content, "text/html")
    message.send()

    return status_code(status=status.HTTP_200_OK)


@periodic_task(run_every=datetime.timedelta(hours=24))
def clean_expired_tokens():
    """
    Clean expired tokens each 24h.
    """

    now = datetime.datetime.now().strftime('%H')
    mode_1 = Tokens.objects.filter(mode=1, is_used=True)
    mode_2 = Tokens.objects.filter(mode=2, is_used=True)
    mode_3 = Tokens.objects.filter(mode=3, is_used=True)

    for token in mode_1:
        offset = token.created_at + datetime.timedelta(hours=1)

        if offset.strftime('%H') == now:
            token.delete()

    for token in mode_2:
        offset = token.created_at + datetime.timedelta(hours=24)

        if offset.strftime('%H') == now:
            token.delete()

    for token in mode_3:
        offset = token.created_at + datetime.timedelta(hours=3)

        if offset.strftime('%H') == now:
            token.delete()

    return status_code(status=status.HTTP_204_NO_CONTENT)
