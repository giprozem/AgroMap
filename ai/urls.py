from django.urls import path

from ai.views.predicted_contour import CutAPIView
from ai.views.productivity import CheckAPIView, CreatingIndexAPIView

urlpatterns = [
    path('cut/', CutAPIView.as_view()),
    path('check/', CheckAPIView.as_view()),
    path('creating/', CreatingIndexAPIView.as_view()),
]
