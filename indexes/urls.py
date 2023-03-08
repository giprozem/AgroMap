from django.urls import path

from indexes.views import ContourYearAPIView, CreatingAverage, ActualIndexesOfContourYear, SatelliteImagesDate
from indexes.views.download_satelite_images import DownloadAPIView
from indexes.views.generated_indexes import CreatingVegIndexesAPIView

urlpatterns = [
    path('average/', CreatingAverage.as_view()),
    path('download/', DownloadAPIView.as_view()),
    path('creating-veg-indexes/', CreatingVegIndexesAPIView.as_view()),
    path('actual-veg-indexes/', ActualIndexesOfContourYear.as_view()),
    path('contour-veg-index-statistics', ContourYearAPIView.as_view()),
    path('satellite_dates/<int:index>/<int:contour>/', SatelliteImagesDate.as_view()),
]
