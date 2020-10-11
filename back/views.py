"""
Error views.
"""

# Dajngo libraries
from django.shortcuts import render


def handler400(request, exception):
    """
    handler 400 error.
    """

    return render(request, '400.html')


def handler403(request, exception):
    """
    handler 403 error.
    """

    return render(request, '403.html')


def handler404(request, exception):
    """
    handler 404 error.
    """

    return render(request, '404.html')


def handler_csrf_failure(request, reason=''):
    """
    handler CSRF failure.
    """

    return render(request, 'csrf_error.html')
