from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from hub.models import LandInfo


@admin.register(LandInfo)
class LandInfoAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    list_display = ['id', 'ink_code']
