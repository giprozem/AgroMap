from django.urls import path

from indexes.views import CreatingAverage, ActualIndexesOfContourYear, SatelliteImagesDate, ContourAPIView, \
    ContourProductivityPredictAPIView, ActualIndexesOfContourAI, PredictedSatelliteImagesDate
from indexes.views.download_satellite_images import DownloadSatelliteImagesV2

urlpatterns = [
    # Mapping of URL paths to corresponding views.
    # Route for creating average contour value.
    path('average/', CreatingAverage.as_view()),
    # Route for retrieving vegetation indices for a given contour based on its ID.
    path('actual-veg-indexes/', ActualIndexesOfContourYear.as_view()),
    path('ai-actual-veg-indexes/', ActualIndexesOfContourAI.as_view()),
    path('contour-veg-index-statistics/', ContourAPIView.as_view()),
    path('satellite_dates/<int:index>/<int:contour>/', SatelliteImagesDate.as_view()),
    path('ai-satellite_dates/<int:index>/<int:contour>/', PredictedSatelliteImagesDate.as_view()),
    path('productivity-predict/', ContourProductivityPredictAPIView.as_view()),
    # Route for downloading satellite images (Version 2).
    path('v2/download_satellite_images/', DownloadSatelliteImagesV2.as_view()),
]
