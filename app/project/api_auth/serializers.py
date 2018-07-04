from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import environ
from datetime import datetime, timedelta

from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name','last_name','country', 'user')
        read_only_fields = ('user','first_name','last_name')
        required_fields =  ('country',)

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(max_length=32,
                                     validators=[UniqueValidator(
                                         queryset=User.objects.all())]
                                     )

    password = serializers.CharField(
        min_length=8, required=True, write_only=True)

    user_profile = UserProfileSerializer()

    def create(self, validated_data):

        user_profile = validated_data.pop('user_profile')

        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            is_active=validated_data['is_active'])

        user_profile['user'] = user
        UserProfile.objects.create(**user_profile)
         
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email',  'password', 'is_active','user_profile')
        required_fields = ('username', 'password', 'email',)
        write_onlny_fields = ('is_active','password','email','user_profile')

class UserReadSerializer(serializers.ModelSerializer):
    user_profile = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='country'
     )
    class Meta:
        model = User
        fields = ('id','email','user_profile')
        

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        print(token)
        # Add custom claims

        print(token)

        return token
