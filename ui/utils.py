"""
Utils UI.
"""

# Modules
from back.settings import HOST

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
        url = 'https://backproject.xyz/services/'
        return post(url, data=data, headers=headers).json()

    elif data['types'] == 'date':
        url = 'https://backproject.xyz/releases/'
        return post(url, data=data, headers=headers).json()

    elif data['types'] == 'coming_soon':
        url = 'https://backproject.xyz/releases/'
        return get(url, headers=headers).json()

    elif data['types'] == 'uuid':
        url = 'https://backproject.xyz/services/{}/{}/'.format(data['service'], data['uuid'])
        return get(url, headers=headers)
