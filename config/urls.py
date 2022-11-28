from schema_graph.views import Schema
from config import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from gip.views.calculate_polygon import StatisticsAPIView
from gip.views.conton import ContonViewSet
from gip.views.contour import ContourViewSet, PointAPIView
from gip.views.crop_yield import CropYieldViewSet
from gip.views.culture import CultureViewSet
from gip.views.district import DistrictViewSet
from gip.views.region import RegionViewSet

router = DefaultRouter()
router.register('contour', ContourViewSet)
router.register('region', RegionViewSet)
router.register('district', DistrictViewSet)
router.register('conton', ContonViewSet)
router.register('culture', CultureViewSet)
router.register('crop_yield', CropYieldViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='API PLOT',
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('docs/', schema_view.with_ui()),
    path("schema/", Schema.as_view()),
    path("get_point", PointAPIView.as_view()),
    path("statistics", StatisticsAPIView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Agromap'
# admin.site.site_title = 'Mysite Admin Panel'