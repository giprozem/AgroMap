from django.contrib.gis import admin

from gip.models import District
from leaflet.admin import LeafletGeoAdmin


@admin.register(District)
class DistrictAdmin(LeafletGeoAdmin):
    list_display = ['id', 'name', 'region', 'created_by', 'updated_by']
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_filter = ('region', 'name', )
    ordering = ('name', 'created_at')
    list_per_page = 20
    search_fields = ('name', 'region')
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'name', )

