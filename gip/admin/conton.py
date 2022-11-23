from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from gip.models import Conton


@admin.register(Conton)
class ContonAdmin(LeafletGeoAdmin):
    readonly_fields = ('created_at', 'updated_at')
