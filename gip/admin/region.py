from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import Region


@admin.register(Region)
class RegionAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    list_display = ('id', 'name', 'population', 'area', 'density', )
    readonly_fields = ('id', 'created_at', 'updated_at', )
    list_filter = ('name', 'population', 'area', 'density', )
    ordering = ('name', 'created_at', )
    list_per_page = 20
    search_fields = ('name', 'population', 'area', 'density', )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'name', )
