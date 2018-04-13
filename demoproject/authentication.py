from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.authentication import (
    SessionAuthentication,)

from account.serializers import UserSerializer, User
from account.constants import ACCOUNT_CREDENTIAL_MESSAGE, ACCOUNT_REMOVED_MESSAGE,\
    ACCOUNT_INACTIVE_MESSAGE


def update_or_create_token(self, request, user_obj):
    token, created = Token.objects.get_or_create(user=user_obj)
    return token.key


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


def authenticate_user(self, request, username, password, user_type):
    try:
        username = username.strip()
        user_type = user_type.strip().lower()
        user_obj = User.objects.get(username__iexact=username, user_type=user_type)
    except User.DoesNotExist:
        raise NotFound('No account exists by username %s'% username )

    if user_obj.is_deleted:
        raise PermissionDenied(ACCOUNT_REMOVED_MESSAGE)
    elif user_obj.is_active:
        auth_user = authenticate(username=username.lower(), password=password)
        if auth_user:
            login(request, user_obj)
            context = {
                'request': request,
            }
            user = UserSerializer(instance=user_obj, context=context)
            data = user.data
            data['token'] = update_or_create_token(self, request, user_obj)
            data['last_login'] = None

            if user_obj.last_login:
                data['last_login'] = user_obj.last_login.strftime(
                    "%Y-%m-%dT%H:%M:%S%z")
            return Response(data)
        else:
            raise PermissionDenied(ACCOUNT_CREDENTIAL_MESSAGE)
    else:
        raise PermissionDenied(ACCOUNT_INACTIVE_MESSAGE)

def logout_user(self, request):
    if request.user and request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response(
            {'message': 'Successfully Logged out'},
            status=status.HTTP_200_OK)
    else:
        return Response(status=401)
