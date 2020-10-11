"""
Status code service.
"""

# Django REST framework
from rest_framework import status

# Models
from models.models import Users, Histories, Favorites


def status_code(**kwargs):
    """
    It gonna returns the status code
    generated on the request.
    """

    return {
        'status': kwargs.get('status'),
        'details': kwargs.get('details')
    }


def create_item(user, data, mode):
    """
    Create an history or favorite
    item.
    """

    try:
        if mode == 'history':
            item = Histories.objects.get_or_create(
                user=user,
                service=data['service'],
                types=data['types'],
                search=data.get('search'),
                year=data.get('year'),
                month=data.get('month')
            )

        elif mode == 'favorite':
            item = Favorites.objects.get_or_create(
                user=user,
                types=data['types'],
                uuid=data['uuid'],
                title=data['title'],
                release_date=data['release_date'],
                duration=data.get('duration'),
                description=data.get('description'),
                rating=data.get('rating'),
                image_cover=data.get('image_cover')
            )

        return status_code(status=status.HTTP_201_CREATED, details=item)

    except (KeyError, TypeError, Users.DoesNotExist):
        return status_code(
            status=status.HTTP_401_UNAUTHORIZED,
            details='User or uuid not provided.'
        )


def delete_item(user, data, mode):
    """
    Delete an history or favorite
    item.
    """

    try:
        if mode == 'history':
            Histories.objects.filter(
                user=user,
                pk=data['uuid']
            ).delete()

        elif mode == 'history_all':
            Histories.objects.filter(
                user=user
            ).delete()

        elif mode == 'favorite':
            Favorites.objects.filter(
                user=user,
                uuid=data['uuid']
            ).delete()

        elif mode == 'favorite_all':
            Favorites.objects.filter(
                user=user
            ).delete()

        return status_code(status=status.HTTP_204_NO_CONTENT)

    except (KeyError, TypeError, Users.DoesNotExist):
        return status_code(
            status=status.HTTP_401_UNAUTHORIZED,
            details='User or uuid not provided.'
        )
