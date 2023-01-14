from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from indexes.models.satelliteimage import SatelliteImages


@admin.register(SatelliteImages)
class SatelliteImagesAdmin(SimpleHistoryAdmin):
    readonly_fields = ('id', 'bbox', )
