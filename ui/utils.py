"""
Utils UI.
"""

# Modules
from back.settings import REAL_HOST

# Utilities
from requests import get, post


def api(request, data):
    """
    POST request to the endpoint
    `services:search`, return the
    response in json format.
    """

    headers = {'Accept': 'application/json; version=v1'}

    if request.user.is_authenticated:
        headers['Authorization'] = request.session['token']['Authorization']
        headers['Secret'] = request.session['token']['Secret']

    if data['types'] == 'search_all':
        url = '{}/services/'.format(REAL_HOST)
        return post(url, data=data, headers=headers).json()

    elif data['types'] == 'date':
        url = '{}/releases/'.format(REAL_HOST)
        return post(url, data=data, headers=headers).json()

    elif data['types'] == 'coming_soon':
        url = '{}/releases/'.format(REAL_HOST)
        return get(url, headers=headers).json()

    elif data['types'] == 'uuid':
        url = '{}/services/{}/{}/'.format(REAL_HOST, data['service'], data['uuid'])
        return get(url, headers=headers)
