"""
Urlpatterns services.
"""

# Django
from django.urls import path

# Views
from api.services import views


urlpatterns = [
    path(
        route='',
        view=views.SearchView.as_view(),
        name='search'
    ),

    path(
        route='releases/',
        view=views.ReleasesView.as_view(),
        name='releases'
    ),

    path(
        route='movieseries/<slug:uuid>/',
        view=views.MovieSeriesView.as_view(),
        name='movieseries'
    ),

    path(
        route='games/<slug:uuid>/',
        view=views.GamesView.as_view(),
        name='games'
    ),

    path(
        route='music/<slug:uuid>/',
        view=views.MusicView.as_view(),
        name='music'
    ),

    path(
        route='history/',
        view=views.HistoryView.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy_all'
        }),
        name='history_list_or_create_or_delete_all'
    ),

    path(
        route='history/<slug:uuid>/',
        view=views.HistoryView.as_view({'delete': 'destroy'}),
        name='history_delete'
    ),

    path(
        route='favorites/',
        view=views.FavoritesView.as_view({
            'get': 'list',
            'delete': 'destroy_all'
        }),
        name='favorite_list_or_delete_all'
    ),

    path(
        route='favorites/<slug:uuid>/',
        view=views.FavoritesView.as_view({'post': 'create', 'delete': 'destroy'}),
        name='favorite_create_or_delete'
    )
]
