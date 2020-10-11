"""
Serializers services.
"""

# Django REST Framework
from rest_framework import serializers, status

# Models
from models.models import Histories, Favorites

# Modules
from api.auths.utils import get_authentication, decode_token
from api.services.utils import (
    UtilsMoviesAndSeries,
    UtilsGames,
    UtilsMusic
)
from api.services.commons import create_item, delete_item, status_code

# Global variables
movieseries = UtilsMoviesAndSeries()
games = UtilsGames()
music = UtilsMusic()

SERVICE_TYPES = [
    'movieseries',
    'games',
    'music',
    'all'
]
TYPES = [
    'search_all',
    'date',
    'uuid',
    'coming_soon'
]


class HistoryModelSerializer(serializers.ModelSerializer):
    """
    History model serializer.
    """

    class Meta:
        """
        Fields of the model `Histories`.
        """

        model = Histories
        fields = (
            'pk',
            'service',
            'types',
            'search',
            'year',
            'month'
        )


class SearchSerialzer(HistoryModelSerializer):
    """
    Search serializer.
    """

    service = serializers.ChoiceField(
        choices=SERVICE_TYPES,
        label='Service',
        help_text='Filtering by service (movieseries, game, music).'
    )

    types = serializers.ChoiceField(
        choices=TYPES,
        label='Type',
        help_text='Search by type (movieseries, game, music).'
    )

    search = serializers.CharField(
        min_length=1,
        max_length=250,
        label='Search',
        help_text='Search field.'
    )

    def validate(self, data):
        """
        Validate if the params are
        corrects.
        """

        try:
            data['service']
            data['search']

            if data['types'] in ['date', 'uuid', 'coming_soon']:
                raise serializers.ValidationError(
                    'Not supported `{}` field, check out if the endpoint is rigth.'.format(
                        data['types']
                    )
                )

        except (KeyError, TypeError):
            raise serializers.ValidationError(
                'Missing fileds (`service`, `types`, `search`)'
            )

        request = self.context['request']
        self.context['data'] = data or request.query_params

        return data

    def services(self):
        """
        Search by all services.
        """

        data = self.context['data']

        if data['service'] == 'movieseries':
            return self.retrieve(movieseries)

        elif data['service'] == 'games':
            return self.retrieve(games)

        elif data['service'] == 'music':
            return self.retrieve(music)

        elif data['service'] == 'all':
            return self.retrieve('all')

    def retrieve(self, svc):
        """
        Search only by movies or series.
        """

        data = self.context['data']

        if data['types'] == 'search_all':
            return svc.search_all(data)

        elif data['types'] == 'date':
            return svc.search_date(data)

        elif data['types'] == 'uuid':
            return svc.search_uuid(data)

        elif data['types'] == 'coming_soon':
            return {
                1: movieseries.search_coming_soon(),
                2: games.search_coming_soon(),
                3: music.search_coming_soon()
            }

    def create(self):
        """
        It will create an history
        item only if the user is
        authenticated.
        """

        request = self.context['request']

        if not request.user.is_authenticated:
            return status_code(status=status.HTTP_401_UNAUTHORIZED)

        return create_item(
            get_authentication(request),
            self.context['data'],
            'history'
        )


class SearchReleaseSerializer(SearchSerialzer):
    """
    Search only by date serializer.
    """

    search = serializers.CharField(required=False)

    def validate(self, data):
        """
        Validate if the params are
        corrects.
        """

        try:
            data['service']
            data['year']

            if data['types'] in ['search_all', 'uuid', 'coming_soon']:
                raise serializers.ValidationError(
                    'Not supported `{}` field, check out if the endpoint is rigth.'.format(
                        data['types']
                    )
                )

        except (KeyError, TypeError):
            raise serializers.ValidationError(
                'Missing fileds (`service`, `types`, `year`).'
            )

        request = self.context['request']
        self.context['data'] = data or request.query_params

        return data


class SearchUUIDSerializer(SearchSerialzer):
    """
    Search by only uuif serializer.
    """

    search = serializers.CharField(required=False)

    def validate(self, data):
        """
        Get only the uuid.
        """

        request = self.context['request']
        slug = self.context.get('kwargs') or request.query_params
        data['uuid'] = slug.get('uuid')
        self.context['data'] = data

        return data


class SearchNotRequiredSerializer(SearchSerialzer):
    """
    Search not required serializer
    """

    service = serializers.CharField(required=False)
    types = serializers.CharField(required=False)
    search = serializers.CharField(required=False)

    def validate(self, data):
        """
        Get the slug.
        """

        slug = self.context.get('kwargs')
        data['uuid'] = slug.get('uuid')
        self.context['data'] = data

        return data

    def destroy(self):
        """
        It will delete an history
        item only if the user is
        authenticated.
        """

        request = self.context['request']

        if not request.user.is_authenticated:
            return status_code(status=status.HTTP_401_UNAUTHORIZED)

        return delete_item(
            get_authentication(request),
            self.context['data'],
            'history'
        )


class SearchDeleteAllSerializer(serializers.Serializer):
    """
    Search delete all serializer.
    """

    authorization = serializers.CharField(
        min_length=25,
        label='Authorization',
        help_text='Authorization field'
    )

    secret = serializers.CharField(
        min_length=25,
        label='Secret',
        help_text='Secret field'
    )

    def validate(self, data):
        """
        Validate data.
        """

        token = decode_token(data['authorization'], data['secret'], 1)

        if token['username'] != self.context['request'].user.username:
            raise serializers.ValidationError('Invalid keys')

        self.context['data'] = data

        return data

    def destroy_all(self):
        """
        It will delete all
        history items.
        """

        request = self.context['request']

        if not request.user.is_authenticated:
            return status_code(status=status.HTTP_401_UNAUTHORIZED)

        return delete_item(
            get_authentication(request),
            self.context['data'],
            'history_all'
        )


class FavoriteModelSerializer(serializers.ModelSerializer):
    """
    Favorite model serializer.
    """

    class Meta:
        """
        Fields of the model `Favorites`.
        """

        model = Favorites
        fields = (
            'types',
            'uuid',
            'title',
            'release_date',
            'duration',
            'description',
            'rating',
            'image_cover'
        )


class FavoriteCreateSerializer(FavoriteModelSerializer):
    """
    Favorite delete serializer.
    """

    uuid = serializers.CharField(required=False)

    def validate(self, data):
        """
        Validate data to the model.
        """

        data['uuid'] = self.context['kwargs']['uuid']
        data = FavoriteModelSerializer(data).data
        self.context['data'] = data

        return data

    def create(self):
        """
        It will create an favorite
        item only if the user is
        authenticated.
        """

        request = self.context['request']

        if not request.user.is_authenticated:
            return status_code(status=status.HTTP_401_UNAUTHORIZED)

        return create_item(
            get_authentication(request),
            self.context['data'],
            'favorite'
        )


class FavoriteDestorySerializer(serializers.Serializer):
    """
    Favorite destroy serializer.
    """

    def validate(self, data):
        """
        Validate uuid field.
        """

        data['uuid'] = self.context['kwargs']['uuid']
        self.context['data'] = data

        return data

    def destroy(self):
        """
        It will delete an favorite
        item only if the user is
        authenticated.
        """

        request = self.context['request']

        if not request.user.is_authenticated:
            return status_code(status=status.HTTP_401_UNAUTHORIZED)

        return delete_item(
            get_authentication(request),
            self.context['data'],
            'favorite'
        )


class FavoriteDestroyAllSerializer(serializers.Serializer):
    """
    Favorite destroy all serialzer.
    """

    authorization = serializers.CharField(
        min_length=25,
        label='Authorization',
        help_text='Authorization field'
    )

    secret = serializers.CharField(
        min_length=25,
        label='Secret',
        help_text='Secret field'
    )

    def validate(self, data):
        """
        Validate data.
        """

        token = decode_token(data['authorization'], data['secret'], 1)

        if token['username'] != self.context['request'].user.username:
            raise serializers.ValidationError('Invalid keys')

        self.context['data'] = data

        return data

    def destroy_all(self):
        """
        It will delete all
        favorite items.
        """

        request = self.context['request']

        if not request.user.is_authenticated:
            return status_code(status=status.HTTP_401_UNAUTHORIZED)

        return delete_item(
            get_authentication(request),
            self.context['data'],
            'favorite_all'
        )
