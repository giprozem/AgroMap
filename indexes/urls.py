from rest_framework.routers import DefaultRouter

from indexes.views import ContourYearViewSet

router = DefaultRouter()
router.register('contour-veg-index-statistics', ContourYearViewSet)
urlpatterns = router.urls
