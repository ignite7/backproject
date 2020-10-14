"""
Base urlpatterns.
"""

# Django
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    # Admin
    path(
        'admin/doc/',
        include('django.contrib.admindocs.urls')
    ),

    path(
        'admin/',
        admin.site.urls
    ),

    # UI
    path(
        '',
        include(
            ('ui.urls', 'ui'),
            namespace='ui'
        )
    ),

    # Services
    path(
        'services/',
        include(
            ('api.services.urls', 'services'),
            namespace='services'
        )
    ),

    # Auths
    path(
        'auth/',
        include(
            ('api.auths.urls', 'auth'),
            namespace='auth'
        )
    )

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handle request errors
handler400 = 'back.views.handler400'

handler403 = 'back.views.handler403'

handler404 = 'back.views.handler404'
