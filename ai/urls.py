from django.urls import path, include

from ai.views.predicted_contour import CutAPIView, Contour_AIViewSet, Contour_AIInScreen
from ai.views.productivity import CheckAPIView, CreatingIndexAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('contour', Contour_AIViewSet)


urlpatterns = [
    path('cut/', CutAPIView.as_view()),
    path('check/', CheckAPIView.as_view()),
    path('creating/', CreatingIndexAPIView.as_view()),
    path('contour-in-screen/', Contour_AIInScreen.as_view()),
    path('', include(router.urls)),
]

"""
dasdassaad
"""