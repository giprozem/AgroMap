from django.urls import path, include

from hub.views.elevation_and_soil import ElevationSoilAPIView
from hub.views.land_info import LandInfoSearch
from hub.views.zem_balance_api import AsrEniCodeAPIView
from hub.views.authetificated import LoginHubView
from rest_framework.routers import DefaultRouter
from hub.views.zem_balance_api import ZemBalanceViewSet


router = DefaultRouter()

#Zem Balance
router.register('zem_balance', ZemBalanceViewSet, basename='zem_balance')


urlpatterns = [
    path('get-eni-code/', AsrEniCodeAPIView.as_view()),
    path('search_ink_hub/', LandInfoSearch.as_view()),
    path('login_hub/', LoginHubView.as_view()),
    path('elevation/', ElevationSoilAPIView.as_view()),
    path('', include(router.urls)),
]
