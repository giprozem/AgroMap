from django.urls import path, include

from gip.views.contact_information import DepartmentViewSet, ContactInformationViewSet
from gip.views.conton import ContonAPIView
from gip.views.contour import (
    FilterContourAPIView,
    ContourStatisticsAPIView,
    StatisticsContourProductivityAPIView,
    MapContourProductivityAPIView,
    CoordinatesPolygonAPIView,
    ContourSearchAPIView,
    AuthDetailContourViewSet,
    CultureStatisticsAPIView,
)
from gip.views.district import DistrictAPIView
from gip.views.polygon_and_point_in_polygon import (
    OccurrenceCheckAPIView,
    PolygonsInBbox,
    PolygonsInScreen,
)
from gip.views.region import RegionAPIView
from gip.views.soil import SoilAPIView, SoilClassAPIView
from gip.views.statistics import GraphicTablesAPIView, CulturePercentAPIView
from gip.views.culture import CultureViewSet
from gip.views.landtype import LandTypeAPIView
from gip.views.shapefile import UploadShapefileApiView, ExportShapefileApiView, import_shapefile, export_all_data_shapefile
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("contour", AuthDetailContourViewSet)
router.register("culture", CultureViewSet)
router.register("department", DepartmentViewSet)
router.register("contact-information", ContactInformationViewSet)

urlpatterns = [
    # Soil-related URLs
    path("soil-creating/", SoilAPIView.as_view()),
    # Occurrence check URL
    path("occurrence-check/", OccurrenceCheckAPIView.as_view()),
    # Graphic tables URL
    path("graphic-tables/", GraphicTablesAPIView.as_view()),
    # Culture percent URL
    path("culture-percent/", CulturePercentAPIView.as_view()),
    # Polygons in Bbox URL
    path("polygons-in-bbox/", PolygonsInBbox.as_view()),
    # Filter Contour URL
    path("filter_contour/", FilterContourAPIView.as_view()),
    # Contour statistics URL
    path("contour-statistics/", ContourStatisticsAPIView.as_view()),
    # Culture statistics URL
    path("culture-statistics/", CultureStatisticsAPIView.as_view()),
    # Contour statistics productivity URL
    path(
        "contour-statistics-productivity/",
        StatisticsContourProductivityAPIView.as_view(),
    ),
    # Contour map productivity URL
    path("contour-map-productivity/", MapContourProductivityAPIView.as_view()),
    # Coordinates Polygon URL
    path("coordinates-polygon/", CoordinatesPolygonAPIView.as_view()),
    # Contour search URL
    path("contour-search/", ContourSearchAPIView.as_view()),
    # Polygons in Screen URL
    path("polygons-in-screen/", PolygonsInScreen.as_view()),
    # Region-related URLs
    path("region/", RegionAPIView.as_view()),
    # District-related URLs
    path("district/", DistrictAPIView.as_view()),
    # Conton-related URL
    path("conton/", ContonAPIView.as_view()),
    # Land Type URL
    path("land-type/", LandTypeAPIView.as_view()),
    # DefaultRouter URLs (contour, culture, department, contact-information)
    path("", include(router.urls)),
    # Soil Class URL
    path("soil-class/", SoilClassAPIView.as_view()),
    # Shapefile Upload URL
    path(
        "shapefile/upload/", UploadShapefileApiView.as_view(), name="shapefile-upload"
    ),
    # Shapefile Export URL
    path(
        "shapefile/export/", ExportShapefileApiView.as_view(), name="shapefile-export"
    ),
    path('admin/contour/import/', import_shapefile, name='import_shapefile'),
    path('admin/contour/export/', export_all_data_shapefile, name='export_shapefile'),
]
