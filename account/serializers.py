from rest_framework import serializers
from rest_framework.exceptions import NotAcceptable
from .profile_utils import check_valid_password,email_validation
from django.core.validators import EmailValidator
from .models import *


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
        serializer to create user's basic information
    """
    confirm_password = serializers.CharField(required=False)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id','user_type', 'first_name', 'last_name',
            'email', 'password', 'confirm_password',
            'phone_number')
        write_only_fields = ('password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # verify password and confirm_password match
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        if not (password == confirm_password):
            raise NotAcceptable(
                "password and confirm_password don't match."
            )
        user_email = validated_data['email']
        if not email_validation(user_email):
            raise NotAcceptable("Not a Valid Email Address.")


        user = User.objects.filter(email__iexact=user_email).first()
        if not check_valid_password(password):
            raise NotAcceptable('Password field is not acceptable.')
        elif user and user.is_active:
            raise NotAcceptable(
                "You are already registered with us. Please log into your account."
            )
        elif user and not user.is_active:
            # if user is not activated but created an account
            # allow user to update the data
            user.user_type = validated_data['user_type']
            user.first_name = validated_data['first_name']
            user.last_name = validated_data['last_name']
            user.email = validated_data['email']
            user.is_active = True
        elif not user:
            user = User.objects.create(
                user_type=validated_data['user_type'],
                username=validated_data['email'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
        user.set_password(password)
        # user.is_verified = False

        user.save()
        return user


    def validate(self, attrs):
        attrs = super(UserSerializer, self).validate(attrs)
        fields = [
            'user_type', 'first_name', 'last_name',
            'email', 'password', 'confirm_password',
            'phone_number']
        for i in range(0, 7):
            if fields[i] not in attrs:
                raise serializers.ValidationError(
                    {fields[i]: "{} is required".format(fields[i])}
                )

        return attrs

class UserListSerializer(serializers.HyperlinkedModelSerializer):
    """
        serializer to retrieve all details of course
    """
    class Meta:
        model = User
        fields = (
            'id', 'url', 'user_type', 'first_name', 'last_name',
            'email', 'profile_assigned_roles', 'profile_assigned_permissions',
            'is_active','created_at')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
        serializer to retrieve all details of course
    """
    class Meta:
        model = User
        fields = (
            'id', 'url', 'user_type', 'first_name', 'last_name',
            'email')


class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    """
        serializer to retrieve all details of course
    """
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'is_active', 'phone_number')

class UserFaqSerializer(serializers.HyperlinkedModelSerializer):
    """
        serializer to retrieve all details FAQ according to user_type
    """
    class Meta:
        model = Faq
        fields = ('user_type','faq','faq_answer','created_by','created_at','updated_at')

