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
from decimal import Decimal

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

    def get_object(self, pk):
        try:
            return TeamEvent.objects.get(pk=pk)
        except TeamEvent.DoesNotExist:
            raise Http404

    def post(self, request, format=None):

        bulk = isinstance(request.data, list)
        if bulk:
            serializer = TeamEventSerializer(data=request.data, many=True)
            if serializer.is_valid():
                instance = serializer.save()
                read_serializer = TeamEventReadSerializer(instance, many=True)
                return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,  frmat=None):
        validated = []
        ok_response = []
        errors = []

        for data in request.data:
            pk = data['id']
            db_team_event = self.get_object(pk)
            serializer = TeamEventSerializer(db_team_event, data=data)
            if serializer.is_valid():
                validated.append(serializer)
            else:
                errors.append(serializer.errors)

        if not errors:
            for serializer in validated:
                instance = serializer.save()
                read_serializer = TeamEventReadSerializer(instance)
                ok_response.append(read_serializer.data)
            return Response(ok_response)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        team_event = self.get_object(pk)
        team_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserTeamEventPredictionCreate(APIView):

    schema = get_predictor_schema()

    def get_object(self, pk):
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
            return Response([], status=status.HTTP_200_OK)

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
                instance = serializer.save()
                read_serializer = UserTeamEventPredictionReadSerializer(
                    instance, many=True)
                return Response(read_serializer.data, status=status.HTTP_201_CREATED)
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
                instance = serializer.save()
                read_serializer = UserTeamEventPredictionReadSerializer(
                    instance, many=True)
                return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        user = request.user
        validated = []
        ok_response = []
        errors = []
        for data in request.data:
            if 'id' in data:
                pk = data['id']
                db_prediction = self.get_object(pk)

                if db_prediction.team_event.started:
                    errors.append({'error': 'event: id: {} already starded'.format(
                        db_prediction.team_event.event.id)})
                    continue

                serializer = UserTeamEventPredictionSerializer(
                    db_prediction, data=data, partial=True)
                if serializer.is_valid():
                    serializer.validated_data['user'] = user
                    validated.append(serializer)
                else:
                    errors.append(serializer.errors)
            else:
                errors.append(
                    {'error': 'Id is requiered in order to perform an update'})

        if not errors:
            for serializer in validated:
                instance = serializer.save()
                read_serializer = UserTeamEventPredictionReadSerializer(
                    instance)
                ok_response.append(read_serializer.data)
            return Response(ok_response)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def check_prediction(self, user, data):
        prediction = self.get_user_team_prediction(
            user.id, data['team'].id, data['result_type'].id)
        return bool(prediction)




class UserTeamEventPredictionUpdate(APIView):

    def get_user_prediction(self, user_id, result_type_id, event_id):
        return UserTeamEventPrediction.objects.filter(user_id=user_id, result_type__id=result_type_id, team_event__event__id=event_id)

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
            data.user.id, data.result_type.id, data.team_event.event.id)

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
            if 'id' in data:
                pk = data['id']
                db_prediction = self.get_prediction(pk)
                serializer = UserGlobalPredictionSerializer(
                    db_prediction, data=data)
                if serializer.is_valid():
                    serializer.validated_data['user'] = user
                    validated.append(serializer)
                else:
                    errors.append(serializer.errors)
            else:
                errors.append(
                    {'error': 'Id is requiered in order to perform an update'})

        if not errors:
            for serializer in validated:
                serializer.save()
                ok_response.append(serializer.data)
            return Response(ok_response)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardView(APIView):

    DEPENDENT = 'dependent'

    def get_predictions(self, user_id):
        return UserTeamEventPrediction.objects.filter(user__id = user_id, calculated=False,  team_event__completed=True)


    def get(self, request, format=None):
        leaderboard = UserLeaderboard.objects.all()
        serializer = UserLeaderboardReadSerializer(leaderboard, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        if not request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        users = User.objects.all()

        leaderboard = []

        leaderboard_update = []

        predictions_update = []

        no_changes = False

        for user in users:

            user_predictions = self.get_predictions(user.id)

            if user_predictions:
                
                checked = False
                delta_check = False
                user_position = UserLeaderboard.objects.filter(user__id=user.id)
                
                if not user_position:
                    user_position = UserLeaderboard(user = user, points=0, delta_points=0.0)
                    user_position.save()
                else:
                    user_position = user_position[0]

                points = user_position.points
                deltas = Decimal(user_position.delta_points)

                for user_prediction in user_predictions:
                    prediction = user_prediction.prediction.lstrip().lower()
                    final_result = user_prediction.team_event.result.lstrip().lower()
                    # wait for the second result to add points

                    user_prediction.calculated = True
                    user_prediction.save(update_fields=['calculated'])

                    if user_prediction.result_type.result_type == self.DEPENDENT and not checked:
                        checked = True
                        continue


                    if prediction == final_result:
                        point = user_prediction.result_type.points
                        points += point

                        if not delta_check:
                            delta = user_prediction.delta
                            deltas = delta + deltas
                            delta_check = True


                    checked = False
                    delta_check = False
                    

                update = {
                    'id': user_position.id,
                    'user':user.id,
                    'points':points,
                    'delta_points':deltas
                }

                leaderboard.append((user_position,update))

        if bool(leaderboard):
            ok_response = []
            errors = []
            for original, update in leaderboard:
                serializer = UserLeaderboardSerializer(original, data=update)
                if serializer.is_valid():
                    instance = serializer.save()
                    read_serializer = UserLeaderboardReadSerializer(instance)
                    ok_response.append(read_serializer.data)
                else:
                    errors.append(serializer.errors)
            return Response(ok_response, status=status.HTTP_200_OK)
        return Response({'message':'no changes for the leaderboard'})


class UserPredictionPointsView(APIView):

    def get_user_points(self, user_id):
        points = UserLeaderboard.objects.filter(user__id = user_id)
        return {'points': points[0].points}

    def get(self, request, format=None):
        return Response(self.get_user_points(request.user.id), status=status.HTTP_200_OK)
