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

    def get(self, request, team_id, event_id, format=None):
        team_event = self.get_team_event(team_id, event_id)
        if team_event:
            serializer = TeamEventReadSerializer(team_event, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

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

    def get_prediction(self, pk):
        try:
            return UserTeamEventPrediction.objects.get(pk=pk)
        except UserTeamEventPrediction.DoesNotExist:
            raise Http404

    def get_user_team_prediction(self, user_id, team_id, result_type_id):
        return UserTeamEventPrediction.objects.filter(user_id=user_id, team__id=team_id, result_type__id=result_type_id)

    def get_user_predictions(self, user_id):
        return UserTeamEventPrediction.objects.filter(user__id=user_id)

    def get(self, request, format=None):
        predictions = self.get_user_predictions(request.user.id)
        if predictions:
            user_predictions = UserTeamEventPredictionReadSerializer(
                predictions, many=True)
            return Response(user_predictions.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        bulk = isinstance(request.data, list)
        if bulk:
            user = request.user
            serializer = UserTeamEventPredictionSerializer(
                data=request.data, many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    data['user'] = user
                    if self.check_prediction(user, data):
                        return Response(
                            {'error': 'prediction already exists'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = request.user
            serializer = UserTeamEventPredictionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['user'] = user
                if self.check_prediction(user, data):
                    return Response(
                        {'error': 'prediction already exist'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        user = request.user
        validated = []
        ok_response = []
        errors = []
        for data in request.data:
            pk = data['id']
            db_prediction = self.get_prediction(pk)
            serializer = UserTeamEventPredictionSerializer(
                db_prediction, data=data)
            if serializer.is_valid():
                serializer.validated_data['user'] = user
                validated.append(serializer)
            else:
                errors.append(serializer.errors)

        if not errors:
            for serializer in validated:
                serializer.save()
                ok_response.append(serializer.data)
            return Response(ok_response)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def check_prediction(self, user, data):
        prediction = self.get_user_team_prediction(
            user.id, data['team'].id, data['result_type'].id)
        return bool(prediction)


class UserTeamEventPredictionUpdate(APIView):

    def get_user_prediction(self, user_id, result_type_id):
        return UserTeamEventPrediction.objects.filter(user_id=user_id, result_type__id=result_type_id)

    def get_prediction(self, pk):
        try:
            return UserTeamEventPrediction.objects.get(pk=pk)
        except UserTeamEventPrediction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        prediction = self.get_prediction(pk)
        serializer = UserTeamEventPredictionReadSerializer(prediction)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = request.user
        prediction = self.get_prediction(pk)
        serializer = UserTeamEventPredictionReadSerializer(
            prediction, request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = user
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        data = self.get_prediction(pk)
        predictions = self.get_user_prediction(
            data.user.id, data.result_type.id)

        if predictions:
            for prediction in predictions:
                prediction.delete()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserGlobalPredictionView(APIView):

    def get_global_prediction(self, user_id):
        return UserGlobalPrediction.objects.filter(user__id=user_id)

    def get(self, request, format=None):
        user = request.user
        global_prediction = self.get_global_prediction(user.id)
        if global_prediction:
            serializer = UserGlobalPredictionReadSerializer(
                global_prediction, many=True)
            if serializer.is_valid():
                return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        bulk = isinstance(request.data, list)
        if bulk:
            user = request.user
            serializer = UserGlobalPredictionSerializer(
                request.data, many=True)
            if serializer.is_valid():
                for data in serializer.validated_data:
                    data['user'] = user
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        user = request.user
        validated = []
        ok_response = []
        errors = []
        for data in request.data:
            pk = data['id']
            db_prediction = self.get_prediction(pk)
            serializer = UserGlobalPredictionSerializer(
                db_prediction, data=data)
            if serializer.is_valid():
                serializer.validated_data['user'] = user
                validated.append(serializer)
            else:
                errors.append(serializer.errors)

        if not errors:
            for serializer in validated:
                serializer.save()
                ok_response.append(serializer.data)
            return Response(ok_response)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
