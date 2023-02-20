from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from schema_graph.views import Schema

from config import settings
from culture_model.views import IndexPlanWithAPIView
from account.views.authenticated import LoginAgromapView
from gip.views.conton import ContonViewSet
from gip.views.contour import LandTypeViewSet, ContourSearchAPIView, \
    ContourStatisticsAPIView, StatisticsContourProductivityAPIView, ContourYearViewSet, \
    MapContourProductivityAPIView, CoordinatesPolygonAPIView, AuthDetailContourYearViewSet, AuthDetailContourViewSet
from gip.views.contour import ContourViewSet, FilterContourAPIView, PastureClassAPIView
from gip.views.crop_yield import CropYieldViewSet
from gip.views.culture import CultureViewSet
from gip.views.district import DistrictViewSet
from gip.views.land_use import LandUseViewSet
from gip.views.owner_details import OwnerDetailsAPIView
from gip.views.polygon_and_point_in_polygon import OccurrenceCheckAPIView, PolygonsInBbox
from gip.views.region import RegionViewSet
from gip.views.script_for_saving_to_db import GeojsonSavingToDBAPIView
from gip.views.statistics import StatisticsAPIView, ContourCultureAPIView, GraphicTablesAPIView, CulturePercentAPIView
from hub.views.authetificated import LoginHubView
from hub.views.land_info import LandInfoSearch
from hub.views.zem_balance_api import ZemBalanceViewSet
from indexes.views import Creating, CreatingAverage, AllIndexesCreating
from indexes.views.actual_veg_index import IndexFactListCreateAPIView, SatelliteImagesDate, ActualIndexesOfContourYear
from indexes.views.download_satelite_images import DownloadAPIView

router = DefaultRouter()
router.register('land-type', LandTypeViewSet)
router.register('contour', ContourViewSet, basename='contour')
router.register('auth-contour', AuthDetailContourViewSet, basename='auth-contour')
router.register('contour_year', ContourYearViewSet, basename='contour_year')
router.register('auth-contour-year', AuthDetailContourYearViewSet, basename='auth-contour-year')
router.register('land-use', LandUseViewSet, basename='land-use')
router.register('region', RegionViewSet)
router.register('district', DistrictViewSet)
router.register('conton', ContonViewSet)
router.register('culture', CultureViewSet)
router.register('crop_yield', CropYieldViewSet)
#Zem Balance
router.register('zem_balance', ZemBalanceViewSet, basename='zem_balance')


schema_view = get_schema_view(
    openapi.Info(
        title='API Agromap and Hub',
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('docs/', schema_view.with_ui()),
    path("schema/", Schema.as_view()),
    path("occurrence-check/", OccurrenceCheckAPIView.as_view()),
    path("statistics/", StatisticsAPIView.as_view()),
    path("contour-culture/", ContourCultureAPIView.as_view()),
    path("graphic-tables/", GraphicTablesAPIView.as_view()),
    path("owner-details/", OwnerDetailsAPIView.as_view()),
    path("culture-percent/", CulturePercentAPIView.as_view()),
    path("index-plan/", IndexPlanWithAPIView.as_view()),
    path("polygons-in-bbox/", PolygonsInBbox.as_view()),
    path("index/", IndexFactListCreateAPIView.as_view()),
    path('login_hub/', LoginHubView.as_view()),
    path('login_agromap/', LoginAgromapView.as_view()),
    path('search_ink_hub/', LandInfoSearch.as_view()),
    path('satellite_dates/<int:index>/<int:contour>/', SatelliteImagesDate.as_view()),
    path('geojson_to_db/', GeojsonSavingToDBAPIView.as_view()),
    path('filter_contour/', FilterContourAPIView.as_view()),
    path('creating/', Creating.as_view()),
    path('average/', CreatingAverage.as_view()),
    path('pasture-class-group/', PastureClassAPIView.as_view()),
    path('contour-search/', ContourSearchAPIView.as_view()),
    path('contour-statistics/', ContourStatisticsAPIView.as_view()),
    path('contour-statistics-productivity/', StatisticsContourProductivityAPIView.as_view()),
    path('contour-map-productivity/', MapContourProductivityAPIView.as_view()),
    path('actual-veg-indexes/', ActualIndexesOfContourYear.as_view()),
    path('all-indexes/', AllIndexesCreating.as_view()),
    path('coordinates-polygon/', CoordinatesPolygonAPIView.as_view()),
    path('hub/', include("hub.urls")),
    path('', include('indexes.urls')),
    path('download/', DownloadAPIView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'AgroMap'
admin.site.index_title = "Эталонная база данных Гипрозем"
