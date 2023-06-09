from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ai.views.heat_map_ndvi import HeatMapAPIView
from ai.views.predict_culture import CulturePredict, PivotTableCulture
from ai.views.create_dataset import CreateAPIView, CreateDescriptionAPIView
from ai.views.predicted_contour import SearchAPIView, Contour_AIViewSet, Contour_AIInScreen, TestYolo, \
    CleanContourCreateDistrictView
from ai.views.productivity import PredictingProductivityAPIVie

router = DefaultRouter()
router.register('contour', Contour_AIViewSet)

urlpatterns = [
    path('search-contour/', SearchAPIView.as_view()),
    path('contour-in-screen/', Contour_AIInScreen.as_view()),
    path('create-dataset/', CreateAPIView.as_view()),
    path('', include(router.urls)),
    path('culture-predict/', CulturePredict.as_view()),
    path('pivot_table_culture/', PivotTableCulture.as_view()),
    path('predict-productivity/', PredictingProductivityAPIVie.as_view()),
    path('heat-map/', HeatMapAPIView.as_view()),
    path('instruction/', CreateDescriptionAPIView.as_view()),
    path('test_yolo/', TestYolo.as_view()),
    path('clean/', CleanContourCreateDistrictView.as_view()),
]
