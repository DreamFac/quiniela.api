from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .schemas import get_predictor_schema

# Create your views here.


class ResultTypeViewSet(viewsets.ModelViewSet):
    queryset = ResultType.objects.all()
    serializer_class = ResultTypeSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


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

    def get_team_event(self, team_id, event_id):
        return TeamEvent.objects.filter(team__id=team_id, event__id=event_id)

    def post(self, request, team_id, event_id, format=None):
        team = self.get_team(team_id)
        event = self.get_event(event_id)

        serializer = TeamEventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['team'] = team
            serializer.validated_data['event'] = event
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, team_id, event_id, format=None):
        team = self.get_team(team_id)
        event = self.get_event(event_id)

        team_event = self.get_team_event(team_id, event_id)

        if team_event is None:
            return Response({'error': 'team event not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TeamEventSerializer(
            team_event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.validated_data['team'] = team
            serializer.validated_data['event'] = event
            # update logic for user prediction
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        team_event = self.get_object(pk)
        team_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserTeamEventPredictionCreate(APIView):

    schema = get_predictor_schema()

    def get(self, request, format=None):
        predictions = UserTeamEventPredictionSerializer(
            UserTeamEventPrediction.objects.all(), many=True)
        return Response(predictions.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        serializer = UserTeamEventPredictionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTeamEventPredictionUpdate(APIView):

    def get_prediction(self, pk):
        try:
            return UserTeamEventPrediction.objects.get(pk=pk)
        except UserTeamEventPrediction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        prediction = self.get_prediction(pk)
        serializer = UserTeamEventPredictionSerializer(prediction)
        return Response(serializer.data)

    def put(self, request, pk, format=None):

        user = request.user
        prediction = self.get_prediction(pk)
        serializer = UserTeamEventPredictionSerializer(
            prediction, request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = user
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        prediction = self.get_prediction(pk)
        prediction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserGlobalPredictionViewSet(APIView):

    def post(self, request, user_id, format=None):
        pass
