# Import necessary modules and classes from Django
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import views from the 'ai' app
from ai.views.heat_map_ndvi import HeatMapAPIView
from ai.views.predict_culture import PivotTableCulture
from ai.views.create_dataset import CreateAPIView, CreateDescriptionAPIView
from ai.views.predicted_contour import SearchAPIView, Contour_AIViewSet, Contour_AIInScreen, PredictedContourAPIView, \
    CleanContourCreateDistrictView
from ai.views.productivity import PredictingProductivityAPIVie

# Create a DefaultRouter for API endpoints
router = DefaultRouter()
router.register('contour', Contour_AIViewSet)

# Define URL patterns
urlpatterns = [
    # Endpoint for searching contours
    path('search-contour/', SearchAPIView.as_view()),

    # Endpoint for displaying contours on the screen
    path('contour-in-screen/', Contour_AIInScreen.as_view()),

    # Endpoint for creating datasets
    path('create-dataset/', CreateAPIView.as_view()),

    # Default router endpoints for 'contour' model, including CRUD operations
    path('', include(router.urls)),

    # Endpoint for creating pivot tables for culture
    path('pivot_table_culture/', PivotTableCulture.as_view()),

    # Endpoint for predicting productivity
    path('predict-productivity/', PredictingProductivityAPIVie.as_view()),

    # Endpoint for displaying a heat map
    path('heat-map/', HeatMapAPIView.as_view()),

    # Endpoint for providing instructions (possibly related to descriptions)
    path('instruction/', CreateDescriptionAPIView.as_view()),

    # Endpoint for predicted contours
    path('predicted_contour/', PredictedContourAPIView.as_view()),

    # Endpoint for cleaning contours and creating districts
    path('clean/', CleanContourCreateDistrictView.as_view()),
]
