from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from gip.models.soil import SoilClass, SoilClassMap, SoilProductivity, SoilFertility


@admin.register(SoilClass)
class SoilClassAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SoilClassMap)
class SoilClassMapAdmin(LeafletGeoAdmin):
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SoilProductivity)
class SoilProductivityAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SoilFertility)
class SoilFertilityAdmin(LeafletGeoAdmin):
    readonly_fields = ('created_at', 'updated_at')
