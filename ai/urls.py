from django.urls import path

from ai.views.predicted_contour import CutAPIView, PredictAPIView

urlpatterns = [
    path('cut/', CutAPIView.as_view()),
    path('predict/', PredictAPIView.as_view()),
]
