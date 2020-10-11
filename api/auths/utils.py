"""
Commons auths.
"""

# Django REST framework
from rest_framework import status, exceptions

# Django
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout, login, authenticate

# Models
from models.models import Users, Tokens

# Modules
from api.services.commons import status_code

# PyJWT
import jwt

# Utilities
import datetime
import secrets


def get_authentication(request):
    """
    Receive the token or cookie
    request and returns the user.
    """

    try:
        authorization = (
            request.META['HTTP_AUTHORIZATION'] or
            request.session['token']['Authorization']
        )
        secret = (
            request.META['HTTP_SECRET'] or
            request.session['token']['Secret']
        )
        token = decode_token(authorization, secret, 1)
        user = token['token'].user

    except (KeyError, TypeError):
        user = request.user

    if user.username != request.user.username:
        raise exceptions.PermissionDenied(status.HTTP_403_FORBIDDEN)

    return user


def login_user(data, request):
    """
    Logging in the user.
    """

    user = authenticate(
        username=data['email'],
        password=data['password']
    )

    if not user or not user.verified_email:
        return None

    token = create_token(user.username, 1, request)
    login(request, user)

    return {'user': user, 'token': token}


def logout_user(username, mode, request):
    """
    Logging out the user.
    """

    if not request.user.is_authenticated:
        raise exceptions.NotAuthenticated(status.HTTP_401_UNAUTHORIZED)

    if request.user.username != username:
        raise exceptions.PermissionDenied(status.HTTP_403_FORBIDDEN)

    delete_token(username, mode)
    request.session.flush()
    logout(request)


def create_token(username, mode, request):
    """
    Returns a token dict.
    """

    check_token = Tokens.objects.filter(
        user__username=username,
        mode=mode
    )

    if check_token.exists():
        if request.user.is_authenticated:
            logout_user(username, mode, request)
        else:
            delete_token(username, mode)

    if mode == 1:
        exp_date = datetime.datetime.now() + datetime.timedelta(hours=1)

    elif mode == 2:
        exp_date = datetime.datetime.now() + datetime.timedelta(hours=24)

    elif mode == 3:
        exp_date = datetime.datetime.now() + datetime.timedelta(hours=3)

    payload = {
        'username': username,
        'mode': mode,
        'diff': secrets.token_hex(20),
        'exp': exp_date.timestamp()
    }

    new_secret = secrets.token_hex(64)
    new_key = jwt.encode(payload=payload, key=new_secret, algorithm='HS256')
    hash_secret = make_password(new_secret)
    hash_key = make_password(new_key.decode())

    try:
        Tokens.objects.create(
            user=Users.objects.get(username=username),
            mode=mode,
            key=hash_key,
            secret=hash_secret,
        )

    except Users.DoesNotExist:
        raise exceptions.AuthenticationFailed(status.HTTP_401_UNAUTHORIZED)

    token = {
        'Authorization': 'Token {}'.format(new_key.decode()),
        'Secret': new_secret
    }
    request.session['token'] = token

    return token


def delete_token(username, mode):
    """
    Delete token of the
    user when is requeried.
    """

    try:
        Tokens.objects.get(
            user=Users.objects.get(username=username),
            mode=mode
        ).delete()

        return status_code(status=status.HTTP_204_NO_CONTENT)

    except Users.DoesNotExist:
        raise exceptions.NotFound(status.HTTP_404_NOT_FOUND)


def decode_token(key, secret, mode):
    """
    Returns the payload of the
    token.
    """

    try:
        payload = jwt.decode(
            jwt=key.split()[1],
            key=secret,
            algorithm='HS256'
        )

        if mode != payload['mode']:
            raise exceptions.NotAcceptable(status.HTTP_406_NOT_ACCEPTABLE)

        token = Tokens.objects.get(
            user=Users.objects.get(username=payload['username']),
            mode=mode
        )

        check_key = check_password(key.split()[1], token.key)
        check_secret = check_password(secret, token.secret)

        if not check_key or not check_secret:
            raise exceptions.NotAuthenticated(status.HTTP_401_UNAUTHORIZED)

    except (Tokens.DoesNotExist, Users.DoesNotExist):
        raise exceptions.NotFound(status.HTTP_404_NOT_FOUND)

    except jwt.ExpiredSignatureError:
        raise exceptions.PermissionDenied(status.HTTP_403_FORBIDDEN)

    except jwt.exceptions.PyJWTError:
        raise exceptions.ParseError(status.HTTP_400_BAD_REQUEST)

    return {
        'username': payload['username'],
        'mode': payload['mode'],
        'token': token
    }
