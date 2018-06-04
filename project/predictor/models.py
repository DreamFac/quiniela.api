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
    points = models.IntegerField(default=1)
    def __str__(self):
        return self.name


class EventType(BaseModel):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Team(BaseModel):
    name = models.CharField(max_length=150)
    flag = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Event(BaseModel):
    date = models.DateTimeField()
    place = models.CharField(max_length=150)
    event_type = models.ForeignKey(
        EventType, related_name='event_type', on_delete=models.CASCADE)

    def __str__(self):
        return '[ {} ] - [ {} ] - [ {} ]'.format(self.event_type, str(self.date), self.place)


class TeamEvent(BaseModel):

    result_type = models.ForeignKey(
        ResultType, related_name='team_event', on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, related_name='team_event', on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team, related_name='team_event', on_delete=models.CASCADE)
    result = models.CharField(max_length=150)

    started = models.BooleanField(default=False)

    completed = models.BooleanField(default=False)
    

    def __str__(self):
        return 'id: [ {} ] - [ {} ] - [ {} ] - [ {} ]'.format(self.id, self.event, self.result_type, self.result)


class UserTeamEventPrediction(BaseModel):
    user = models.ForeignKey(
        'auth.User', related_name='user_team_event_prediction', on_delete=models.CASCADE)

    team_event = models.ForeignKey(
        TeamEvent, related_name='user_team_event_prediction', on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team, related_name='user_team_event_prediction', on_delete=models.CASCADE)
    result_type = models.ForeignKey(
        ResultType, related_name='user_team_event_prediction', on_delete=models.CASCADE)
    prediction = models.CharField(max_length=150)

    read = models.BooleanField(default=False)

    calculated = models.BooleanField(default=False)

    delta = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)



class UserGlobalPrediction(BaseModel):

    user = models.ForeignKey(
        'auth.User', related_name='user_global_prediction', on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team, related_name='user_global_prediction', on_delete=models.CASCADE)
    place = models.IntegerField()


class UserLeaderboard(BaseModel):

    user = models.ForeignKey(
        'auth.User', related_name='user_leaderboard', on_delete=models.CASCADE)
    
    points = models.BigIntegerField()

    