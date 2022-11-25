from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin
from leaflet.admin import LeafletGeoAdmin

from gip.models import CropYield


@admin.register(CropYield)
class CropYieldAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    list_display = ['id', 'year', 'contour']
    readonly_fields = ('created_at', 'updated_at')
