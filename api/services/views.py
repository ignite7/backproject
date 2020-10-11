"""
Views services.
"""

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

# Models
from models.models import Histories, Favorites

# Selerializers
from api.services.serializers import (
    SearchSerialzer,
    SearchReleaseSerializer,
    SearchNotRequiredSerializer,
    SearchDeleteAllSerializer,
    SearchUUIDSerializer,
    FavoriteModelSerializer,
    FavoriteCreateSerializer,
    FavoriteDestorySerializer,
    FavoriteDestroyAllSerializer
)

# Permission
from api.auths.permission import CheckOwner, CheckVerifiedEmail
from api.services.permission import CheckRequestPerHour

# Modules
from api.auths.utils import get_authentication

# Versioning
from back.versioning import APIVersion

# Utilities
from django_filters.rest_framework import DjangoFilterBackend


class SearchView(APIView):
    """
    Main view.
    """

    http_method_names = ['get', 'post']
    permission_classes = [CheckRequestPerHour]
    versioning_class = APIVersion

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = SearchSerialzer(
            data=request.data or request.query_params,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.services(),
            status=status.HTTP_200_OK,
            headers=serializer.create()
        )


class ReleasesView(APIView):
    """
    Releases view.
    """

    http_method_names = ['get', 'post']
    permission_classes = [CheckRequestPerHour]
    versioning_class = APIVersion

    def get(self, request, *args, **kwargs):
        """
        GET request
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = SearchNotRequiredSerializer(
            data={'service': 'all', 'types': 'coming_soon'},
            context={'request': request, 'kwargs': kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.services(),
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = SearchReleaseSerializer(
            data=request.data or request.query_params,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.services(),
            status=status.HTTP_200_OK,
            headers=serializer.create()
        )


class MovieSeriesView(APIView):
    """
    Movies view.
    """

    http_method_names = ['get']
    permission_classes = [CheckRequestPerHour]
    versioning_class = APIVersion

    def get(self, request, *args, **kwargs):
        """
        GET request
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = SearchUUIDSerializer(
            data={'service': 'movieseries', 'types': 'uuid'},
            context={'request': request, 'kwargs': kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.services(),
            status=status.HTTP_200_OK
        )


class GamesView(APIView):
    """
    Games view.
    """

    http_method_names = ['get']
    permission_classes = [CheckRequestPerHour]
    versioning_class = APIVersion

    def get(self, request, *args, **kwargs):
        """
        GET request
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = SearchUUIDSerializer(
            data={'service': 'games', 'types': 'uuid'},
            context={'request': request, 'kwargs': kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.services(),
            status=status.HTTP_200_OK
        )


class MusicView(APIView):
    """
    Music view.
    """

    http_method_names = ['get']
    permission_classes = [CheckRequestPerHour]
    versioning_class = APIVersion

    def get(self, request, *args, **kwargs):
        """
        GET request
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = SearchUUIDSerializer(
            data={'service': 'music', 'types': 'uuid'},
            context={'request': request, 'kwargs': kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.services(),
            status=status.HTTP_200_OK
        )


class HistoryView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    History view.
    """

    permission_classes = [
        IsAuthenticated,
        CheckVerifiedEmail,
        CheckOwner
    ]
    versioning_class = APIVersion
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend
    )
    search_fields = (
        'user__username',
        'service',
        'types',
        'search',
        'year',
        'month'
    )
    ordering_fields = (
        'service',
        'types',
        'search',
        'year',
        'month',
        'created_at',
        'modified_at'
    )
    ordering = (
        '-year',
        '-month',
        '-created_at',
        '-modified_at'
    )
    filter_fields = ('is_used',)

    def get_queryset(self):
        """
        Get the history of the user.
        """

        user = get_authentication(self.request)
        queryset = Histories.objects.filter(user=user, is_used=True)

        return queryset

    def get_serializer_class(self, *args, **kwargs):
        """
        Get the serializer class depending of the
        request method.
        """

        if self.request.method in ['GET', 'POST']:
            serializer_class = SearchSerialzer

        elif self.action == 'destroy':
            serializer_class = SearchNotRequiredSerializer

        elif self.action == 'destroy_all':
            serializer_class = SearchDeleteAllSerializer

        return serializer_class

    def get(self, request, *args, **kwargs):
        """
        GET request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        POST request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=serializer.create()
        )

    def destroy_all(self, request, *args, **kwargs):
        """
        DELETE all request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            headers=serializer.destroy_all()
        )

    def destroy(self, request, *args, **kwargs):
        """
        DELETE request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data={},
            context={'request': request, 'kwargs': kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            headers=serializer.destroy()
        )


class FavoritesView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    Create favorite items and
    delete them as well.
    """

    permission_classes = [
        IsAuthenticated,
        CheckVerifiedEmail,
        CheckOwner
    ]
    versioning_class = APIVersion
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend
    )
    search_fields = (
        'user__username',
        'types',
        'uuid',
        'title',
        'release_date',
        'duration',
        'description',
        'rating'
    )
    ordering_fields = (
        'types',
        'uuid',
        'title',
        'release_date',
        'duration',
        'description',
        'rating'
        'created_at',
        'modified_at'
    )
    ordering = (
        '-types',
        '-release_date',
        '-duration',
        '-rating',
        '-created_at',
        '-modified_at'
    )
    filter_fields = ('is_used',)

    def get_queryset(self):
        """
        Get the favorite items of the user.
        """

        user = get_authentication(self.request)
        queryset = Favorites.objects.filter(user=user, is_used=True)

        return queryset

    def get_serializer_class(self, *args, **kwargs):
        """
        Get the serializer class depending of the
        request method.
        """

        if self.request.method == 'GET':
            serializer_class = FavoriteModelSerializer

        elif self.request.method == 'POST':
            serializer_class = FavoriteCreateSerializer

        elif self.action == 'destroy':
            serializer_class = FavoriteDestorySerializer

        elif self.action == 'destroy_all':
            serializer_class = FavoriteDestroyAllSerializer

        return serializer_class

    def get(self, request, *args, **kwargs):
        """
        GET request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        return self.list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        POST request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context={'request': request, 'kwargs': kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=serializer.create()
        )

    def destroy_all(self, request, *args, **kwargs):
        """
        DELETE all request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            headers=serializer.destroy_all()
        )

    def destroy(self, request, *args, **kwargs):
        """
        DELETE request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data={},
            context={'request': request, 'kwargs': kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            headers=serializer.destroy()
        )
