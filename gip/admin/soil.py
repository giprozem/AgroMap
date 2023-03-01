from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models.soil import SoilClass, SoilClassMap, SoilProductivity, SoilFertility


@admin.register(SoilClass)
class SoilClassAdmin(SimpleHistoryAdmin, TranslationAdmin):
    list_display = ('ID', 'name', 'description', )
    readonly_fields = ('id', 'created_at', 'updated_at', )
    list_filter = ('name', 'ID', )
    ordering = ('name', 'created_at', )
    list_per_page = 20
    search_fields = ('name', 'ID', )
    date_hierarchy = 'created_at'
    list_display_links = ('name', 'ID', )


@admin.register(SoilClassMap)
class SoilClassMapAdmin(LeafletGeoAdmin, SimpleHistoryAdmin, TranslationAdmin):
    list_display = ('id', 'soil_class', )
    readonly_fields = ('id', 'created_at', 'updated_at', )
    list_filter = ('soil_class', )
    ordering = ('soil_class', 'created_at', )
    list_per_page = 20
    search_fields = ('soil_class', )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'soil_class', )


# @admin.register(SoilProductivity)
# class SoilProductivityAdmin(SimpleHistoryAdmin):
#     list_display = ('id', 'name', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('name', )
#     ordering = ('name', 'created_at', )
#     list_per_page = 20
#     search_fields = ('name', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'name', )


# @admin.register(SoilFertility)
# class SoilFertilityAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
#     list_display = ('id', 'soil_productivity', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('soil_productivity', )
#     ordering = ('soil_productivity', 'created_at', )
#     list_per_page = 20
#     search_fields = ('soil_productivity', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'soil_productivity', )
