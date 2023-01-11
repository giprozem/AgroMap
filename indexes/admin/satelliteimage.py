from django.contrib import admin

from indexes.models import SatelliteImages


@admin.register(SatelliteImages)
class SatelliteImagesAdmin(admin.ModelAdmin):
    pass
