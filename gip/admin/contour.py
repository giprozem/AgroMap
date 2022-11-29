from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import Contour


@admin.register(Contour)
class ContourAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at', 'sum_ha')
    list_display = ('id', 'ink', 'conton', 'farmer', )
    list_filter = ('conton', 'farmer', 'sum_ha', )
    ordering = ('conton', 'created_at')
    list_per_page = 20
    search_fields = ('conton__name', 'farmer__pin_inn', )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'ink', )
