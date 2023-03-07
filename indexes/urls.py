from django.urls import path
from rest_framework.routers import DefaultRouter

from indexes.views import ContourYearViewSet, CreatingAverage, ActualIndexesOfContourYear
from indexes.views.download_satelite_images import DownloadAPIView
from indexes.views.generated_indexes import CreatingVegIndexesAPIView

router = DefaultRouter()
router.register('contour-veg-index-statistics', ContourYearViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('average/', CreatingAverage.as_view()),
    path('download/', DownloadAPIView.as_view()),
    path('creating-veg-indexes/', CreatingVegIndexesAPIView.as_view()),
    path('actual-veg-indexes/', ActualIndexesOfContourYear.as_view()),
]
