from django.contrib import admin
from .models import (
    ResultType,
    TeamEvent,
    Team,
    Event,
    UserTeamEventPrediction,
    UserGlobalPrediction
)
# Register your models here.
admin.site.register(ResultType)
admin.site.register(TeamEvent)
admin.site.register(Team)
admin.site.register(Event)
admin.site.register(UserTeamEventPrediction)
admin.site.register(UserGlobalPrediction)