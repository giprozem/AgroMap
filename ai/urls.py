from django.urls import path

from ai.views.predicted_contour import CutAPIView


urlpatterns = [
    path('cut/', CutAPIView.as_view()),
]
