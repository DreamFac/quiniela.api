from django.contrib import admin
from .models import (
    ResultType,
    TeamEvent,
    Team,
    Event,
    EventType,
    UserTeamEventPrediction,
    UserGlobalPrediction
)

# Admin models


class ResultTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'result_type', 'description','points')
    list_display_links = ('name',)


class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'place', 'event_type')
    list_display_links = ('event_type',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'flag')
    list_display_links = ('name',)

class TeamEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'result_type', 'event', 'team', 'result','completed','started',)
    list_display_links = ('event',)

class UserTeamEventPredictionAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'team_event', 'team', 'result_type', 'prediction', 'read')
    list_display_links = ('team_event',)

# Register your models here.
admin.site.register(ResultType, ResultTypeAdmin)
admin.site.register(TeamEvent, TeamEventAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(UserTeamEventPrediction, UserTeamEventPredictionAdmin)
admin.site.register(UserGlobalPrediction)
