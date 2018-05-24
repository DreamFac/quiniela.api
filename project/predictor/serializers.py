from rest_framework import serializers
from .models import (
    ResultType,
    TeamEvent,
    Team,
    Event,
    EventType,
    UserTeamEventPrediction,
    UserGlobalPrediction
)


class ResultTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultType
        fields = ('id', 'name', 'result_type', 'description')
        required_fields = ('name', 'result_type')

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ('id', 'name', 'description')
        required_fields = ('name',)
        
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'flag',)
        required_fields = ('name','flag',)

class TeamEventSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    class Meta:
        model = TeamEvent
        fields = ('id', 'event', 'team', 'result_type', 'result',)
        required_fields = ('event','team','result_type',)


class EventSerializer(serializers.ModelSerializer):
    team_event = TeamEventSerializer(many=True, read_only = True)
    event_type = EventTypeSerializer(many=False, read_only=True)
    class Meta:
        model = Event
        fields = ('date', 'place','event_type', 'team_event',)
        required_fields =('date','place','event_type',)
        read_only_fields = ('team_event',)

class UserTeamEventPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTeamEventPrediction
        fields = ('user', 'team_event', 'team', 'result_type', 'prediction',)

class UserGlobalPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGlobalPrediction
        fields = ('user','team','place',)