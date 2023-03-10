from django.urls import path

from gip.views.contour import FilterContourAPIView, ContourStatisticsAPIView, StatisticsContourProductivityAPIView, \
    MapContourProductivityAPIView, CoordinatesPolygonAPIView, ContourSearchAPIView
from gip.views.district import DistrictAPIView
from gip.views.geoserver import Geoserver
from gip.views.polygon_and_point_in_polygon import OccurrenceCheckAPIView, PolygonsInBbox, PolygonsInScreen
from gip.views.region import RegionAPIView
from gip.views.soil import SoilAPIView
from gip.views.statistics import GraphicTablesAPIView, CulturePercentAPIView

urlpatterns = [
    path('soil-creating/', SoilAPIView.as_view()),
    path("occurrence-check/", OccurrenceCheckAPIView.as_view()),
    path("graphic-tables/", GraphicTablesAPIView.as_view()),
    path("culture-percent/", CulturePercentAPIView.as_view()),
    path("polygons-in-bbox/", PolygonsInBbox.as_view()),
    path('filter_contour/', FilterContourAPIView.as_view()),
    path('contour-statistics/', ContourStatisticsAPIView.as_view()),
    path('contour-statistics-productivity/', StatisticsContourProductivityAPIView.as_view()),
    path('contour-map-productivity/', MapContourProductivityAPIView.as_view()),
    path('coordinates-polygon/', CoordinatesPolygonAPIView.as_view()),
    path('contour-search/', ContourSearchAPIView.as_view()),
    path('polygons-in-screen/', PolygonsInScreen.as_view()),
    path('geoserver/', Geoserver.as_view()),
    path('region/', RegionAPIView.as_view()),
    path('district/', DistrictAPIView.as_view()),
]
