from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from gip.models import Contour


@admin.register(Contour)
class ContourAdmin(LeafletGeoAdmin):
    list_display = ['id', 'conton', 'sum_ha']
    readonly_fields = ('created_at', 'updated_at', 'sum_ha')

