from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin
from leaflet.admin import LeafletGeoAdmin

from gip.models import CropYield


@admin.register(CropYield)
class CropYieldAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    list_display = ['id', 'culture', 'contour', 'year', 'season']
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('culture', 'contour', 'year', 'season', )
    ordering = ('culture', 'created_at')
    list_per_page = 20
    search_fields = ('culture__name', 'contour__ink', 'year', 'season',)
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'culture', )
