"""
Admin services.
"""

# Django
from django.contrib import admin

# Models
from models.models import Histories, Favorites


@admin.register(Histories)
class HistoriesAdmin(admin.ModelAdmin):
    """
    Admin of the model `Histories`.
    """

    list_display = (
        'pk',
        'user',
        'service',
        'types',
        'search',
        'year',
        'month',
        'is_used',
        'created_at',
        'modified_at'
    )

    list_editable = (
        'service',
        'types',
        'search',
        'year',
        'month',
        'is_used'
    )

    search_fields = (
        'user',
        'service',
        'types',
        'search',
        'year',
        'month'
    )

    list_filter = (
        'service',
        'types',
        'year',
        'month',
        'is_used',
        'created_at',
        'modified_at'
    )

    readonly_fields = (
        'created_at',
        'modified_at'
    )


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    """
    Admin of the model `Favorites`.
    """

    list_display = (
        'pk',
        'user',
        'uuid',
        'title',
        'release_date',
        'duration',
        'description',
        'rating',
        'image_cover',
        'is_used',
        'created_at',
        'modified_at'
    )

    list_editable = (
        'title',
        'release_date',
        'duration',
        'description',
        'rating',
        'image_cover',
        'is_used'
    )

    search_fields = (
        'user',
        'title',
        'release_date',
    )

    list_filter = (
        'release_date',
        'duration',
        'rating',
        'is_used',
        'created_at',
        'modified_at'
    )

    readonly_fields = (
        'created_at',
        'modified_at'
    )
