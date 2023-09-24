# Import necessary modules
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models.soil import SoilClass, SoilClassMap

# Register the SoilClass model with the admin panel
@admin.register(SoilClass)
class SoilClassAdmin(SimpleHistoryAdmin, TranslationAdmin):
    # Define fields to be displayed in the list view
    list_display = ('id_soil', 'name', 'description', 'color',)
    
    # Define read-only fields
    readonly_fields = ('id', 'created_at', 'updated_at',)
    
    # Add filters for the 'name' and 'id_soil' fields in the list view
    list_filter = ('name', 'id_soil',)
    
    # Set the default ordering for the list view
    ordering = ('name', 'created_at',)
    
    # Specify the number of items displayed per page in the list view
    list_per_page = 20
    
    # Add search functionality for 'name', 'id_soil', and 'id' fields
    search_fields = ('name', 'id_soil', 'id')
    
    # Add a date hierarchy based on the 'created_at' field
    date_hierarchy = 'created_at'
    
    # Make 'name' and 'id_soil' fields clickable in the list view
    list_display_links = ('name', 'id_soil',)

# Register the SoilClassMap model with the admin panel
@admin.register(SoilClassMap)
class SoilClassMapAdmin(LeafletGeoAdmin, SimpleHistoryAdmin, TranslationAdmin):
    # Define fields to be displayed in the list view
    list_display = ('id', 'soil_class',)
    
    # Define read-only fields
    readonly_fields = ('id', 'created_at', 'updated_at',)
    
    # Add a filter for the 'soil_class' field in the list view
    list_filter = ('soil_class',)
    
    # Set the default ordering for the list view
    ordering = ('soil_class', 'created_at',)
    
    # Specify the number of items displayed per page in the list view
    list_per_page = 20
    
    # Add a date hierarchy based on the 'created_at' field
    date_hierarchy = 'created_at'
    
    # Make 'id' and 'soil_class' fields clickable in the list view
    list_display_links = ('id', 'soil_class',)
