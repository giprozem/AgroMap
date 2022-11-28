from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import Conton


@admin.register(Conton)
class ContonAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_display = ('id', 'name', 'district', )
    list_filter = ('name', 'district', )
    ordering = ('name', 'created_at')
    list_per_page = 20
    search_fields = ('name', 'district', )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'name', )
