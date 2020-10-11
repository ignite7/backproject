"""
Utilities services.
"""

# Django REST Framework
from rest_framework import status, exceptions

# Spotipy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

# Utilities
from json import JSONDecodeError
from datetime import date
import environ
import requests

# Read the .env file
env = environ.Env()
environ.Env.read_env()


class UtilsMoviesAndSeries:
    """
    Utilities for the service
    of movies and series.
    """

    def search_all(self, data):
        """
        Search by all items.
        """

        try:
            movieseries = {'movieseries': []}
            url = 'https://imdb-api.com/en/API/SearchAll/{}/{}'.format(
                env('API_KEY_MOVIE'),
                data['search']
            )
            response = requests.get(url).json()

            if 'Maximum' in response['errorMessage'].split():
                raise exceptions.Throttled(status.HTTP_429_TOO_MANY_REQUESTS)

            for item in response['results']:
                url = 'https://imdb-api.com/en/API/Title/{}/{}/{}'.format(
                    env('API_KEY_MOVIE'),
                    item['id'],
                    'Images,Trailer'
                )
                movieseries['movieseries'].append(requests.get(url).json())

            return movieseries

        except JSONDecodeError:
            return movieseries

        except (KeyError, TypeError):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required `search` field.'
            )

    def search_date(self, data):
        """
        Search by date.
        """

        try:
            movieseries = {'movieseries': []}
            url = 'https://imdb-api.com/en/API/Keyword/{}/{}'.format(
                env('API_KEY_MOVIE'),
                data['year']
            )
            response = requests.get(url).json()

            if 'Maximum' in response['errorMessage'].split():
                raise exceptions.Throttled(status.HTTP_429_TOO_MANY_REQUESTS)

            for item in response['items']:
                url = 'https://imdb-api.com/en/API/Title/{}/{}/{}'.format(
                    env('API_KEY_MOVIE'),
                    item['id'],
                    'Images,Trailer'
                )
                movieseries['movieseries'].append(requests.get(url).json())

            return movieseries

        except JSONDecodeError:
            return movieseries

        except (KeyError, TypeError):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required `year` field.'
            )

    def search_uuid(self, data):
        """
        Search by uuid.
        """

        try:
            movieseries = {'movieseries': []}
            url = 'https://imdb-api.com/en/API/Title/{}/{}/{}'.format(
                env('API_KEY_MOVIE'),
                data['uuid'],
                'Images,Trailer'
            )
            response = requests.get(url).json()

            if 'Maximum' in response['errorMessage'].split():
                raise exceptions.Throttled(status.HTTP_429_TOO_MANY_REQUESTS)

            movieseries['movieseries'].append(response)

            return movieseries

        except JSONDecodeError:
            return movieseries

        except (KeyError, TypeError):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required `uuid` field.'
            )

    def search_coming_soon(self):
        """
        Search by coming soon.
        """

        try:
            movieseries = {'movieseries': []}
            url = 'https://imdb-api.com/en/API/ComingSoon/{}'.format(
                env('API_KEY_MOVIE')
            )
            response = requests.get(url).json()

            if 'Maximum' in response['errorMessage'].split():
                raise exceptions.Throttled(status.HTTP_429_TOO_MANY_REQUESTS)

            for item in response['items']:
                url = 'https://imdb-api.com/en/API/Title/{}/{}/{}'.format(
                    env('API_KEY_MOVIE'),
                    item['id'],
                    'Images,Trailer'
                )
                movieseries['movieseries'].append(requests.get(url).json())

            return movieseries

        except JSONDecodeError:
            return movieseries

        except (KeyError, TypeError):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required `comingsoon` field.'
            )


class UtilsGames:
    """
    Utilities for the service
    of games.
    """

    url = 'https://api.igdb.com/v4/games'
    token_url = (
        'https://id.twitch.tv/oauth2/token?client_id={}&'
        'client_secret={}&grant_type=client_credentials'
    ).format(env('CLIENT_ID_GAMES'), env('CLIENT_SECRET_GAMES'))
    token = requests.post(token_url).json()['access_token']
    headers = {
        'Accept': 'application/json',
        'Client-ID': env('CLIENT_ID_GAMES'),
        'Authorization': 'Bearer {}'.format(token)
    }

    def search_all(self, data):
        """
        Search by all items.
        """

        try:
            games = {}
            query = (
                'search *"{}"*;'
                'fields id, name, genres.name, first_release_date,'
                'platforms.name, summary, dlcs.name,expansions.name,'
                'total_rating, keywords.name, age_ratings.synopsis, similar_games.name,'
                'similar_games.cover.url, cover.url, screenshots.url,'
                'videos.video_id, websites.url;'
                'limit 20;'
            ).format(data['search'])
            games['games'] = requests.post(
                self.url,
                headers=self.headers,
                data=query
            ).json()

            return games

        except (TypeError, KeyError):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required `search` field.'
            )

    def search_date(self, data):
        """
        Search by date.
        """

        try:
            games = {}
            query = (
                'fields id, name, genres.name, first_release_date,'
                'platforms.name, summary, dlcs.name, expansions.name,'
                'total_rating, keywords.name, age_ratings.synopsis, similar_games.name,'
                'similar_games.cover.url, cover.url, screenshots.url,'
                'videos.video_id, websites.url;'
                'where release_dates.y = {} & release_dates.m = {};'
                'sort first_release_date desc;'
                'limit 20;'
            ).format(
                data['year'],
                data['month']
            )
            games['games'] = requests.post(
                self.url,
                headers=self.headers,
                data=query
            ).json()

            return games

        except (TypeError, KeyError):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required (`year`, `month`) fields.'
            )

    def search_uuid(self, data):
        """
        Search by uuid.
        """

        try:
            games = {}
            query = (
                'fields id, name, genres.name, first_release_date,'
                'platforms.name, summary, dlcs.name, expansions.name,'
                'total_rating, keywords.name, age_ratings.synopsis, similar_games.name,'
                'similar_games.cover.url, cover.url, screenshots.url,'
                'videos.video_id, websites.url;'
                'where id = {};'
                'sort first_release_date desc;'
                'limit 1;'
            ).format(data['uuid'])
            games['games'] = requests.post(
                self.url,
                headers=self.headers,
                data=query
            ).json()

            return games

        except (TypeError, KeyError):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required `uuid` field.'
            )

    def search_coming_soon(self):
        """
        Search by coming soon.
        """

        try:
            games = {}
            today = date.today()

            query = (
                'fields id, name, genres.name, first_release_date,'
                'platforms.name, summary, dlcs.name, expansions.name,'
                'total_rating, keywords.name, age_ratings.synopsis, similar_games.name,'
                'similar_games.cover.url, cover.url, screenshots.url,'
                'videos.video_id, websites.url;'
                'where release_dates.y > {} & release_dates.m > {};'
                'sort first_release_date desc;'
                'limit 20;'
            ).format(
                today.strftime('%Y'),
                today.strftime('%m').lstrip('0')
            )
            games['games'] = requests.post(
                self.url,
                headers=self.headers,
                data=query
            ).json()

            return games

        except (TypeError, KeyError):
            raise exceptions.ValidationError(status.HTTP_404_NOT_FOUND)


class UtilsMusic:
    """
    Utilities for the service
    of music.
    """

    manager = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=env('CLIENT_ID_SPOTIFY'),
            client_secret=env('CLIENT_SECRET_SPOTIFY')
        )
    )

    def search_all(self, data):
        """
        Search by all items.
        """

        try:
            music = {}
            music['music'] = self.manager.search(
                q=data['search'],
                limit=20,
                type='track'
            )

            return music

        except (TypeError, KeyError, SpotifyException):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required `search` field.'
            )

    def search_date(self, data):
        """
        Search by date.
        """

        try:
            music = {}
            music['music'] = self.manager.featured_playlists(
                timestamp='{}-{}-01T00:00:00'.format(
                    data['year'],
                    data['month']
                ),
                limit=20
            )

            return music

        except (TypeError, KeyError, SpotifyException):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required (`year`, `month`) fields.'
            )

    def search_uuid(self, data):
        """
        Search by uuid.
        """

        music = {}

        try:
            music['music'] = self.manager.track(data['uuid'])
            return music
        except (TypeError, KeyError, SpotifyException):
            raise exceptions.ValidationError(
                code=status.HTTP_400_BAD_REQUEST,
                detail='It\'s required `uuid` field.'
            )

    def search_coming_soon(self):
        """
        Search by coming soon.
        """

        try:
            music = {}
            music['music'] = self.manager.new_releases(limit=20)

            return music

        except (TypeError, KeyError, SpotifyException):
            raise exceptions.ValidationError(status.HTTP_404_NOT_FOUND)
