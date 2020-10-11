"""
Views auths.
"""

# Dajngo REST framework
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Serializers
from api.auths.serializers import (
    SignupSerializer,
    LoginSerializer,
    LogoutSerializer,
    ConfirmEmailSerializer,
    ResetPasswordSerializer,
    ResetPasswordUpdateSerializer,
    AccountSerializer,
    AccountDeleteSerializer,
    AccountNotRequiredSerializer
)

# Permissions
from api.auths.permission import CheckOwner, CheckVerifiedEmail

# Versioning
from back.versioning import APIVersion


class SignupView(APIView):
    """
    Signup view.
    """

    http_method_names = ['post']
    versioning_class = APIVersion

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = SignupSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.create(),
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """
    Login view.
    """

    http_method_names = ['post']
    versioning_class = APIVersion

    def post(self, request, *args, **kwargs):
        """
        POST request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.create(),
            status=status.HTTP_202_ACCEPTED
        )


class LogoutView(APIView):
    """
    Logout view.
    """

    http_method_names = ['delete']
    permissions = [
        IsAuthenticated,
        CheckVerifiedEmail
    ]
    versioning_class = APIVersion

    def delete(self, request, *args, **kwargs):
        """
        DELETE request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = LogoutSerializer(
            data={},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            headers=serializer.destroy()
        )


class ConfirmEmailView(APIView):
    """
    Cofirm email view.
    """

    http_method_names = ['put']
    versioning_class = APIVersion

    def put(self, request, *args, **kwargs):
        """
        PUT request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = ConfirmEmailSerializer(
            data={},
            context={'request': request, 'kwargs': kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_202_ACCEPTED,
            headers=serializer.update()
        )


class ResetPasswordView(viewsets.GenericViewSet):
    """
    Reset password view.
    """

    versioning_class = APIVersion

    def get_serializer_class(self, *args, **kwargs):
        """
        Get the serializer class depending of the
        request method.
        """

        if self.request.method == 'POST':
            serializer_class = ResetPasswordSerializer

        elif self.request.method == 'PUT':
            serializer_class = ResetPasswordUpdateSerializer

        return serializer_class

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

    def update(self, request, *args, **kwargs):
        """
        PUT request.
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
            data=serializer.data,
            status=status.HTTP_200_OK,
            headers=serializer.update()
        )


class AccountView(APIView):
    """
    Account view.
    """

    http_method_names = ['get', 'patch', 'delete']
    permission_classes = [
        IsAuthenticated,
        CheckOwner,
        CheckVerifiedEmail
    ]
    versioning_class = APIVersion

    def get(self, request, *args, **kwargs):
        """
        GET request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = AccountNotRequiredSerializer(
            data={},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, *args, **kwargs):
        """
        PATCH request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = AccountSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.validate_empty_values(request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            data=serializer.save(),
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        """
        DELETE request.
        """

        if request.version != 'v1':
            return Response(status=status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED)

        serializer = AccountDeleteSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            headers=serializer.destroy()
        )
