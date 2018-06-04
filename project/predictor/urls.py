from django.conf.urls import url, include
from rest_framework import routers
from project.api_auth import views
from rest_framework.urlpatterns import format_suffix_patterns


from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import  TokenRefreshView

from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register(r'result-types', ResultTypeViewSet)
router.register(r'events', EventViewSet)
router.register(r'event-types', EventTypeViewSet)
router.register(r'teams',TeamViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^team-event/?$', TeamEventView.as_view(), name='team-event'),
    url(r'^points/?$', UserPredictionPointsView.as_view(), name='user-points'),
    url(r'^predictions/?$', UserTeamEventPredictionCreate.as_view(), name='user-prediction-create'),
    url(r'^predictions/(?P<pk>[0-9]+)/?$', UserTeamEventPredictionUpdate.as_view(), name='user-prediction-update'),
    url(r'^leaderboard/?$', LeaderboardView.as_view(), name='leaderboard'),
    url(r'^global-predictions/?$', UserGlobalPredictionView.as_view(), name='leaderboard')
]
