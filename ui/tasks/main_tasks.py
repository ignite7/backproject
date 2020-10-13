"""
Tasks main ui.
"""

# Django REST framework
from rest_framework import status

# Django
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Celery
from celery import shared_task

# Modules
from api.services.commons import status_code
from back.settings import HOST, EMAIL_HOST_USER


@shared_task(max_retries=3)
def send_contact_email(data):
    """
    Send contact email task.
    """

    subject = ' New contact email from {}, <Back.com>'.format(data['name'])
    content = render_to_string('emails/contact_email.html', {
        'data': data,
        'host': HOST
    })
    message = EmailMultiAlternatives(
        subject=subject,
        body=content,
        from_email=data['email'],
        to=[EMAIL_HOST_USER]
    )
    message.attach_alternative(content, "text/html")
    message.send()

    return status_code(status=status.HTTP_200_OK)
