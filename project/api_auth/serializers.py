from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import environ
from datetime import datetime, timedelta

from ..predictor.serializers import (
    UserTeamEventPredictionSerializer,
    UserGlobalPredictionSerializer
)

from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'first_name','last_name','country')
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
        min_length=8, write_only=True, required=True)

    user_prediction = UserTeamEventPredictionSerializer(many=True, read_only = True)
    
    user_global_prediction = UserGlobalPredictionSerializer(many=True, read_only = True)


    def create(self, validated_data):

        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            is_active=validated_data['is_active'])

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email',  'password', 'is_active','user_prediction','user_global_prediction',)
        required_fields = ('username', 'password', 'email',)
        read_only_fields = ('user_prediction','user_global_prediction')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        print(token)
        # Add custom claims

        print(token)

        return token
