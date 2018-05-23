from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
# Create your views here.

class ResultTypeViewSet(viewsets.ModelViewSet):
    queryset = ResultType.objects.all()
    serializer_class = ResultTypeSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer



class TeamEventView(APIView):

    def get_team(self, pk):
        try:
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            raise Http404
    
    def get_event(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get_object(self, pk):
        try:
            return TeamEvent.objects.get(pk=pk)
        except TeamEvent.DoesNotExist:
            raise Http404


    def post(self, request, team_id, event_id, format = None ):
        team = self.get_team(team_id)
        event = self.get_event(event_id)

        serializer = TeamEventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['team'] = team
            serializer.validated_data['event'] = event
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, team_id, event_id, format = None ):
        team = self.get_team(team_id)
        event = self.get_event(event_id)

        serializer = TeamEventSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            serializer.validated_data['team'] = team
            serializer.validated_data['event'] = event
            #update logic for user prediction
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        team_event = self.get_object(pk)
        team_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserTeamEventPredictionViewSet(APIView):

    def post(self, request, user_id , format = None):
        pass


class UserGlobalPredictionViewSet(APIView):


    def post(self, request, user_id , format = None):
        pass