from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from account.models import User


def authenticate_user(self, request, username=None, password=None, user_type=None):
    try:
        if (username and password and user_type):
            user_obj = authenticate(
                username=username, password=password)
    except:
        raise NotFound('Invalid username and/or password.')

    if user_obj:
        if user_obj.is_active:
            login(request, user_obj)
            return user_obj
            # s = UserListSerializer(instance=user_obj)
            # data = s.data
            # data['token'] = get_or_create_token(self, request, user_obj)
            # return Response({'user': data})
        else:
            raise PermissionDenied('Inactive user.')
    else:
        raise NotFound('Invalid username and/or password.')


def logout_user(self, request):
    if request.user and request.user.is_authenticated():
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=401)


def get_or_create_token(self, user_obj):
    token = Token.objects.filter(user=user_obj).first()
    if not token:
        token = Token.objects.create(user=user_obj)
    return token.key
