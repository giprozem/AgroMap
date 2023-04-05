from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ai.views.predict_culture import CulturePredict
from ai.views.create_dataset import CreateAPIView
from ai.views.predicted_contour import CutAPIView, Contour_AIViewSet, Contour_AIInScreen
from ai.views.productivity import CreatingIndexAPIView, CreatingIndexSatellite, PredictingProductivityAPIVie

router = DefaultRouter()
router.register('contour', Contour_AIViewSet)


urlpatterns = [
    path('cut/', CutAPIView.as_view()),
    path('creating/', CreatingIndexAPIView.as_view()),
    path('contour-in-screen/', Contour_AIInScreen.as_view()),
    path('create/', CreateAPIView.as_view()),
    path('', include(router.urls)),
    path('culture/', CulturePredict.as_view()),
    path('index-satelite/', CreatingIndexSatellite.as_view()),
    path('predict-productivity/', PredictingProductivityAPIVie.as_view()),
]
