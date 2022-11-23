from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from gip.models import Village


@admin.register(Village)
class VillageAdmin(LeafletGeoAdmin):
    readonly_fields = ('created_at', 'updated_at')
