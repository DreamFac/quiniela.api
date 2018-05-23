from rest_framework import serializers
from .models import (
    ResultType,
    TeamEvent,
    Team,
    Event,
    UserTeamEventPrediction,
    UserGlobalPrediction
)


class ResultTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResultType
        fields = ('id', 'name', 'result_type', 'description')
        required_fields = ('name', 'result_type')


class TeamEventSerializer(serializers.Serializer):
    class Meta:
        model = TeamEvent
        fields = ('id', 'event', 'team', 'result_type', 'result')
        read_only_fields = ('event','team')


class TeamSerializer(serializers.Serializer):
    team_event = TeamEventSerializer(many=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'flag')


class EventSerializer(serializers.Serializer):
    team_event = TeamEventSerializer(many=True)

    class Meta:
        model = Event
        fields = ('date', 'place')


class UserTeamEventPredictionSerializer(serializers.BaseSerializer):
    class Meta:
        model = UserTeamEventPrediction
        fields = ('user', 'team_event', 'team', 'result_type', 'prediction')


class UserGlobalPredictionSerializer(serializers.Serializer):
    class Meta:
        model = UserGlobalPrediction
        fields = ('user','team','place')