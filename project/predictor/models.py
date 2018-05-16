from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

class ResultType(BaseModel):
    name = models.CharField(max_length=150)
    result_type = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

class Team(BaseModel):

    name = models.CharField(max_length=150)
    flag = models.CharField(max_length=150)


class Event(BaseModel):
    
    date = models.DateField()
    place = models.CharField(max_length=150)

class TeamEvent(BaseModel):

    event = models.ForeignKey(Event, related_name='team_event', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='team_event', on_delete=models.CASCADE)
    result_type = models.ForeignKey(ResultType, related_name='team_event', on_delete=models.CASCADE)
    result = models.CharField(max_length=150)

class UserTeamEventPrediction(BaseModel):
    user = models.ForeignKey('auth.User', related_name='user_team_event_prediction', on_delete=models.CASCADE)

    team_event = models.ForeignKey(TeamEvent, related_name='user_team_event_prediction', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='user_team_event_prediction', on_delete=models.CASCADE)
    result_type = models.ForeignKey(ResultType, related_name='user_team_event_prediction', on_delete=models.CASCADE)
    prediction = models.CharField(max_length=150)

class UserGlobalPrediction(BaseModel):

    user = models.ForeignKey('auth.User', related_name='user_global_prediction', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='user_global_prediction', on_delete=models.CASCADE)
    place = models.IntegerField()