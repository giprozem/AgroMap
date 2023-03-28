from django.urls import path

from indexes.views import CreatingAverage, ActualIndexesOfContourYear, SatelliteImagesDate, ContourAPIView, \
    ContourProductivityPredictAPIView
from indexes.views.generated_indexes import CreatingVegIndexesAPIView

urlpatterns = [
    path('average/', CreatingAverage.as_view()),
    path('creating-veg-indexes/', CreatingVegIndexesAPIView.as_view()),
    path('actual-veg-indexes/', ActualIndexesOfContourYear.as_view()),
    path('contour-veg-index-statistics/', ContourAPIView.as_view()),
    path('satellite_dates/<int:index>/<int:contour>/', SatelliteImagesDate.as_view()),
    path('productivity-predict/', ContourProductivityPredictAPIView.as_view()),
]
