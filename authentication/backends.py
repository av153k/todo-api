import jwt

from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from rest_framework import authentication, exceptions

from .models import User

from django.db.models import Q


class JwtAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        print(token)
        try:
            payload = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms='HS256')
        except:
            msg = "Invalid authentications. Could not decode token!"
            raise exceptions.AuthenticationFailed(msg)
        print("Payload ------", payload)
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = "No user matching this token was found!"
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)


class AuthenticationBackend(BaseBackend):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, identifier, password):
        print("identifier ------", identifier)
        try:
            user = User.objects.get(Q(username=identifier) | Q(
                email=identifier))
        except User.DoesNotExist:
            return None

        return user if user.check_password(password) else None
