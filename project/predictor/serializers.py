from rest_framework import serializers
from ..api_auth.serializers import UserSerializer
from .models import (
    ResultType,
    TeamEvent,
    Team,
    Event,
    EventType,
    UserTeamEventPrediction,
    UserGlobalPrediction,
    UserLeaderboard
)


class ResultTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultType
        fields = ('id', 'name', 'result_type', 'description','points')
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
    class Meta:
        model = TeamEvent
        fields = ('id', 'event', 'team', 'result_type', 'result','started','completed')
        required_fields = ('event','team',)

class TeamEventReadSerializer(TeamEventSerializer):
    team = TeamSerializer()
    result_type = ResultTypeSerializer()

class EventSerializer(serializers.ModelSerializer):
    team_event = TeamEventReadSerializer(many=True, read_only = True)
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = Event
        fields = ('id','date', 'place','event_type', 'team_event',)
        required_fields =('date','place','event_type',)
        read_only_fields = ('team_event',)


class UserTeamEventPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTeamEventPrediction
        fields = ('id','user', 'team_event', 'team', 'result_type', 'prediction','read','delta',)
        required_fields = ('team_event','team','result_type','prediction',)
        write_only_fields = ('calculated',)
        read_only_fields = ('user',)


class UserTeamEventPredictionReadSerializer(UserTeamEventPredictionSerializer):
    team_event = TeamEventReadSerializer()


class UserGlobalPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGlobalPrediction
        fields = ('id','user','team','place',)
        read_only_fields = ('user',)

class UserGlobalPredictionReadSerializer(UserGlobalPredictionSerializer):
    team = TeamSerializer()


class UserLeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLeaderboard
        fields = ('user', 'points', 'delta_points',)


class UserLeaderboardReadSerializer(UserLeaderboardSerializer):
        user = UserSerializer()