from django.contrib.gis import admin

from gip.models import District
from leaflet.admin import LeafletGeoAdmin


@admin.register(District)
class DistrictAdmin(LeafletGeoAdmin):
    readonly_fields = ('created_at', 'updated_at')