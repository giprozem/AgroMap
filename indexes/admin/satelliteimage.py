from django.contrib import admin

from indexes.models import SatelliteImages
from indexes.models.satelliteimage import SatelliteImages


@admin.register(SatelliteImages)
class SatelliteImagesAdmin(admin.ModelAdmin):
    pass
