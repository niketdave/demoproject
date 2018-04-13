from .models import User
# from django.core.files import File
from django.core.files.base import ContentFile
from rest_framework.exceptions import NotFound
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from .auth_utils import get_or_create_token as auth_get_or_create_token
from django.conf import settings
from .constants import (PASSWORD_SPECIAL_CHARACTER_SYNTAX, PASSSWORD_MIN_LENGTH, PASSWORD_DIGIT_ERROR,PASSWORD_LENGTH_ERROR, PASSWORD_LETTER_ERROR, PASSWORD_WHITESPACE_ERROR, PASSWORD_SYMBOL_ERROR, WORD_SET_OF_PASSWORD)
from rest_framework.exceptions import NotAcceptable
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random


def check_duplicate_email(user_email):
    return User.objects.filter(
        email__iexact=user_email).exists()


def check_duplicate_username(username):
    return User.objects.filter(
        username__iexact=username).exists()


def fire_email(subject, msg_html, from_email, to):
    try:
        msg = EmailMultiAlternatives(
            subject, msg_html, from_email, [to])
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
        return True
    except:
        return True

def informing_carrier_email_html(driver_name,carrier,message):
    msg_html = '<p>Hello ' + carrier + '</p>'
    msg_html += '<p>Information from Ten65.</p>'
    msg_html += '<p>'+message+' Added '+driver_name+' driver To Ten65 App</p>'
    msg_html += '<p> Thanks,</p><p> Ten65 Team.</p>'
    return msg_html

def password_reset_email_html(user_obj,request, token):
    if not request.get_host().startswith('localhost'):
        link = request.get_host() + '/resetpassword/' + token
    else:
        link = 'http://localhost:8000/resetpassword/' + token

    msg_html = '<p>Hello ' + user_obj.username + '</p>'
    msg_html += '<p><a href="' + link + \
        '">Click Here</a> to reset your password</p><br>'
    msg_html += '<p> Ignore this message if you have not requested for password change request.</p>'
    msg_html += '<p> Thanks,</p><p> Ten65 Team.</p>'
    return msg_html


def welcome_user_email_html(name, password):
    msg_html = '<p>Hello ' + name + '</p>'
    msg_html += '<p>Welcome to Ten65.</p>'
    msg_html += '<p>Your one time password to login is <strong>' + \
        str(password) + '</strong></p>'
    msg_html += '<p>You will have to change the password on first time login.</p>'
    msg_html += '<p>Login and enjoy Ten65 app.</p>'
    msg_html += '<p> Thanks,</p><p> Ten65 Team.</p>'
    return msg_html


def welcome_driver_email_html(name):
    msg_html = '<p>Hello ' + name + '</p>'
    msg_html += '<p>Welcome to Ten65.</p>'
    msg_html += '<p>This email is only to inform you that you have been added to ten65 application.</p>'
    msg_html += '<p> Thanks,</p><p> Ten65 Team.</p>'
    return msg_html


def user_status_email_html(name, status,driver_name, is_active=None, is_deleted=None, message=None):
    msg_html = '<p>Hello ' + name + '</p>'
    msg_html += '<p>Account has been ' + str(status) + '</p>'
    if message:
        msg_html += '<p> Driver name is :'+driver_name+' and the reason is '+message+' </p>'
    else:
        if is_active == False or is_deleted == True:
            msg_html += '<p>Please contact admin for the account activation.</p>'
    msg_html += '<p> Thanks,</p><p> Ten65 Team.</p>'
    return msg_html


def fleet_status_email_html(name, status, truck, is_active=None, is_deleted=None, message=None):
    msg_html = '<p>Hello ' + name + '</p>'
    msg_html += '<p>Fleet '+ str(truck) +' has been ' + str(status) + '.</p>'
    if message:
        msg_html += 'The reason is '+message+'.</p>'
    else:
        if is_active == False or is_deleted == True:
            msg_html += '<p>Please contact admin/carrier for the account activation.</p>'
    msg_html += '<p> Thanks,</p><p> Ten65 Team.</p>'
    return msg_html


def check_valid_password(password):
    print("bhar valo",password)
    if len(password) < PASSSWORD_MIN_LENGTH or not password:
        raise NotAcceptable(PASSWORD_LENGTH_ERROR)
    elif ' ' in password:
        print(password)
        raise NotAcceptable(PASSWORD_WHITESPACE_ERROR)
    elif not any(char.isdigit() for char in password):
        raise NotAcceptable(PASSWORD_DIGIT_ERROR)
    elif not any(char.isalpha() for char in password):
        raise NotAcceptable(PASSWORD_LETTER_ERROR)
    elif not len(set(PASSWORD_SPECIAL_CHARACTER_SYNTAX).intersection(set(password))) > 0:
        raise NotAcceptable(PASSWORD_SYMBOL_ERROR)
    else:
        return True


def email_validation(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def random_password_generator():
    password = "".join(random.sample(
        WORD_SET_OF_PASSWORD, PASSSWORD_MIN_LENGTH))
    return password
