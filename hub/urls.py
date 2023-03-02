from django.urls import path

from hub.views.land_info import LandInfoSearch
from hub.views.zem_balance_api import AsrEniCodeAPIView

urlpatterns = [
    path('get-eni-code/', AsrEniCodeAPIView.as_view()),
    path('search_ink_hub/', LandInfoSearch.as_view()),
]
