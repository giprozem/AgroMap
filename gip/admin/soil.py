from django.contrib.gis import admin

from gip.models.soil import SoilClass, SoilClassMap, SoilProductivity, SoilFertility


@admin.register(SoilClass)
class SoilClassAdmin(admin.ModelAdmin):
    pass


@admin.register(SoilClassMap)
class SoilClassMapAdmin(admin.ModelAdmin):
    pass


@admin.register(SoilProductivity)
class SoilProductivityAdmin(admin.ModelAdmin):
    pass


@admin.register(SoilFertility)
class SoilFertilityAdmin(admin.ModelAdmin):
    pass