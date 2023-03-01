from django.urls import path
from gip.views.soil import SoilAPIView


urlpatterns = [
    path('soil-creating/', SoilAPIView.as_view()),
]
