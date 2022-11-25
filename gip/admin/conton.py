from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import Conton


@admin.register(Conton)
class ContonAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    readonly_fields = ('created_at', 'updated_at')
