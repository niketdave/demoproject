from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.http import JsonResponse
from django.contrib.auth.decorators import *
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAcceptable,AuthenticationFailed

from .models import *
from .serializers import *
from .permissions import UserPermission
from .swagger_fields import UsersFieldsSwagger
from .constants import RESET_PASSWORD_LINK_ERROR,RESET_PASSWORD_CONFIRM_ERROR,RESET_PASSWORD_SUCCESS_MSG,RECORD_NOT_FOUND_ERROR,USER_NOT_FOUND_ERROR
from account import profile_utils
from demoproject import authentication
from account.forms import *

# from account.account_tables.subadmin_datatable import SubadminTable
# from profilerole.profilerole_table.roles_datatable import RoleTable

# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating

# def subadmin(request):
#     queryset = User.objects.filter(user_type='admin')
#     subadmin = SubadminTable(queryset)
#     return render(request, "account/subadmin_list.html", {'subadmin': subadmin})

# def role(request):
#     queryset = Role.objects.all()
#     role = RoleTable(queryset)
#     return render(request, "profilerole/role_list.html", {'roles': role})

@login_required(login_url="login/")
def home(request):
    return render(request,"home.html")

# @login_required(login_url="login/")
# def roles(request):
#     return render(request,"roles.html")


@login_required(login_url="login/")
def profile(request):
    message = ''
    user_obj = User.objects.filter(
                id=request.user.id).first()
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        # check whether it's valid:
        print(request.POST)
        # print(form.cleaned_data['first_name'])
        print(form.is_valid())
        if form.is_valid():
            if user_obj:
                user_obj.first_name = form.cleaned_data['first_name']
                user_obj.last_name = form.cleaned_data['last_name']
                user_obj.phone_number = form.cleaned_data['phone_number']
                user_obj.save()
                message = "Profile Updated successfully."
            else:
                return render(request,"profile.html",{'message':message})
    if message == "Profile Updated successfully.":
        return render(request,"home.html",{'message':message})
    return render(request,"profile.html",{'user_obj':user_obj})

# @forgotpassword_required(forgotpassword_url="forgot_password/")
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            email = form.cleaned_data['email']
            print(email)
            user_obj = User.objects.filter(
                email__iexact=email).first()
            print(user_obj)
            if user_obj:
                print(request)
                email_list = [user_obj.email,]
                token = utils.create_uuid4_hashed_token()
                user_obj.password_reset_token = token
                user_obj.password_reset_flag = True
                user_obj.save()
                # ----------- Send Email for password reset link  ----- #
                to_email_list =email_list
                msg_html = profile_utils.password_reset_email_html(user_obj,request, token)
                subject = 'Ten65 : Reset Password'
                utils.ten65_send_email(msg_html, to_email_list, subject)
                return render(request,"login.html")
            else:
                return render(request,"forgot_password.html")
            # ----------- Send Email for password reset link  ----- #
        # if a GET (or any other method) we'll create a blank form
    else:
        return render(request,"forgot_password.html")


# @login_required(login_url="login/")
def change_password(request):
    print(request.path)
    print(dir(request))
    """
        Change password when request for password change
    """
    message = ''
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user_obj = User.objects.filter(
                id=request.user.id).first()
            hasError = True

            if user_obj:
                old_password = form.cleaned_data['old_password']
                new_password = form.cleaned_data['new_password']
                confirm_password = form.cleaned_data['confirm_password']

                if not user_obj.check_password(old_password):
                    message = "Original password is wrong."
                elif new_password == confirm_password:
                    user_obj.set_password(new_password)
                    user_obj.save()
                    message = "Password changed successfully."
                    status_code = 200
                    hasError = False
                else:
                    message = 'Password and confirm password do not match.'
                    return render(request,"change_password.html",{'message':message})
            else:
                message = 'Allowed only for the loggedin user.'
                return render(request,"change_password.html",{'message':message})
    if message == "Password changed successfully.":
        return render(request,"login.html",{'message':message})
    return render(request,"change_password.html",{'message':message})


# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
@login_required(login_url="login/")
def home(request):
    return render(request,"home.html")

# Create your views here.
def index(request, reset_token):
    """
        Reset password html page when request for password change
    """
    user_obj = User.objects.filter(
        password_reset_token__exact=reset_token).first()
    if user_obj:
        return render(request, 'account/index.html', {
            "token": reset_token
        })
    else:
        return render(request, 'account/error.html', {
            "message": RESET_PASSWORD_LINK_ERROR
        })


def changePassword(request, reset_token):
    """
        Change password when request for password change
    """
    user_obj = User.objects.filter(
        password_reset_token__exact=reset_token).first()
    if user_obj:
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user_obj.set_password(password)
            user_obj.password_reset_token = ''
            user_obj.password_reset_flag = False
            user_obj.save()
            return render(request, 'account/success.html', {
                "message": RESET_PASSWORD_SUCCESS_MSG
            })
        else:
            return render(request, 'account/error.html', {
                "message": RESET_PASSWORD_CONFIRM_ERROR
            })
    else:
        return render(request, 'account/error.html', {
            "message": RESET_PASSWORD_LINK_ERROR
        })


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)
    custom_route_swagger = UsersFieldsSwagger

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'partial_update':
            serializer_class = UserUpdateSerializer
        elif self.action == 'list':
            serializer_class = UserListSerializer
        elif self.action == 'faq':
            serializer_class = UserFaqSerializer
        return serializer_class

    @list_route(methods=['post'])
    def login(self, request, pk=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        if username and password and user_type:
            return authentication.authenticate_user(
                self, request, username=username,
                password=password, user_type=user_type)
        else:
            raise NotAcceptable("Please provide required parameters.")


    @list_route(methods=['get'], serializer_class=[])
    def logout(self, request, pk=None):
        """
        Logout based on the token in the header for logged in user.
        """
        return authentication.logout_user(self, request)

    @list_route(methods=['get'], serializer_class=[])
    def checkDuplicateEmail(self, request, pk=None):
        """
            check if email already exists.
        """
        user_email = request.query_params.get('email', None)
        if user_email is not None:
            return Response(
                status=status.HTTP_200_OK,
                data={"duplicate": User.objects.filter(
                    email__iexact=user_email).exists()})
        return Response(status=status.HTTP_200_OK, data={"duplicate": True})

    @list_route(methods=['post'])
    def changePassword(self, request, pk=None):
        """
            Change password when request for password change
        """
        user_obj = User.objects.filter(
            id=self.request.user.id).first()
        hasError = True
        if user_obj:
            old_password = request.data.get('old_password', None)
            password = request.data.get('password', None)
            confirm_password = request.data.get('confirm_password', None)

            if not old_password:
                raise NotAcceptable("Old Password field is required.")
            elif not password:
                raise NotAcceptable("Password field is required.")
            elif not confirm_password:
                raise NotAcceptable("Confirm Password field is required.")
            elif not user_obj.check_password(old_password):
                raise NotAcceptable("Original password is wrong.")
            elif not profile_utils.check_valid_password(password):
                raise NotAcceptable("Password is not accepted.")
            elif password == confirm_password:
                user_obj.set_password(password)
                user_obj.save()
                message = "Password changed successfully."
                status_code = 200
                hasError = False
            else:
                raise NotAcceptable('Password and confirm password do not match.')
        else:
            raise AuthenticationFailed('Allowed only for the loggedin user.')
        return Response(status=status_code, data={"detail": message})

    @list_route(methods=['get'], serializer_class=[])
    def checkDuplicateUsername(self, request, pk=None):
        """
            check if username with user type already exists.
        """
        user_name = request.query_params.get('username', None)
        if user_name is not None:
            return Response(
                status=status.HTTP_200_OK,
                data={"duplicate": User.objects.filter(
                    username__iexact=user_name).exists()})
        return Response(status=status.HTTP_200_OK, data={"duplicate": True})


    @list_route(methods=['post'])
    def resetPassword(user_obj, request, pk=None):
        """
            Reset password using email
        """
        user_email = request.query_params.get('email', None)
        try:
            user_obj = User.objects.filter(
                email__iexact=user_email).first()
        except Exception as e:
            user_obj = None

        if user_obj:
            token = utils.create_uuid4_hashed_token()
            user_obj.password_reset_token = token
            user_obj.password_reset_flag = True
            user_obj.save()
            # ----------- Send Email for password reset link  ----- #
            to_email_list = user_obj.email.split(',')
            msg_html = profile_utils.password_reset_email_html(
                user_obj, request, token)
            subject = 'Ten65 : Reset Password'
            utils.ten65_send_email(msg_html, to_email_list, subject)
            # ----------- Send Email for password reset link  ----- #
            return Response(
                {"detail": "Please check your email for the link to reset the password."})
        else:
            raise NotFound("No account exist with the given email address.")



class FaqViewSets(
    mixins.ListModelMixin,
    viewsets.GenericViewSet):

    """
        FAQ Listing API
    """

    queryset = Faq.objects.order_by('id')
    serializer_class = UserFaqSerializer
    permission_classes = (AllowAny,)
    filter_fields = ('user_type',)
