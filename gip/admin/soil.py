from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models.soil import SoilClass, SoilClassMap


@admin.register(SoilClass)
class SoilClassAdmin(SimpleHistoryAdmin, TranslationAdmin):
    list_display = ('id_soil', 'name', 'description', 'color',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    list_filter = ('name', 'id_soil',)
    ordering = ('name', 'created_at',)
    list_per_page = 20
    search_fields = ('name', 'id_soil', 'id')
    date_hierarchy = 'created_at'
    list_display_links = ('name', 'id_soil',)


@admin.register(SoilClassMap)
class SoilClassMapAdmin(LeafletGeoAdmin, SimpleHistoryAdmin, TranslationAdmin):
    list_display = ('id', 'soil_class',)
    readonly_fields = ('id', 'created_at', 'updated_at',)
    list_filter = ('soil_class',)
    ordering = ('soil_class', 'created_at',)
    list_per_page = 20
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'soil_class',)
