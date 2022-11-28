from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from gip.models.soil import SoilClass, SoilClassMap, SoilProductivity, SoilFertility


# @admin.register(SoilClass)
# class SoilClassAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'fertility', 'created_by', 'updated_by', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('name', 'fertility', )
#     ordering = ('name', 'created_at', )
#     list_per_page = 20
#     search_fields = ('name', 'fertility', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'name', )
#
#
# @admin.register(SoilClassMap)
# class SoilClassMapAdmin(LeafletGeoAdmin):
#     list_display = ('id', 'soil_class', 'created_by', 'updated_by', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('soil_class', )
#     ordering = ('soil_class', 'created_at', )
#     list_per_page = 20
#     search_fields = ('soil_class', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'soil_class', )
#
#
# @admin.register(SoilProductivity)
# class SoilProductivityAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'created_by', 'updated_by', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('name', )
#     ordering = ('name', 'created_at', )
#     list_per_page = 20
#     search_fields = ('name', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'name', )
#
#
# @admin.register(SoilFertility)
# class SoilFertilityAdmin(LeafletGeoAdmin):
#     list_display = ('id', 'soil_productivity', 'created_by', 'updated_by', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('soil_productivity', )
#     ordering = ('soil_productivity', 'created_at', )
#     list_per_page = 20
#     search_fields = ('soil_productivity', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'soil_productivity', )
