# Import necessary modules
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models import Region

# Register the Region model with the admin panel
@admin.register(Region)
class RegionAdmin(LeafletGeoAdmin, SimpleHistoryAdmin, TranslationAdmin):
    # Define fields to be displayed in the list view
    list_display = ('id', 'code_soato', 'name', 'population', 'area', 'density',)
    
    # Define read-only fields
    readonly_fields = ('id', 'created_at', 'updated_at',)
    
    # Add filters for the 'name', 'population', 'area', and 'density' fields in the list view
    list_filter = ('name', 'population', 'area', 'density',)
    
    # Set the default ordering for the list view
    ordering = ('name', 'created_at',)
    
    # Specify the number of items displayed per page in the list view
    list_per_page = 20
    
    # Add search functionality for 'name', 'population', 'area', and 'density' fields
    search_fields = ('name', 'population', 'area', 'density',)
    
    # Add a date hierarchy based on the 'created_at' field
    date_hierarchy = 'created_at'
    
    # Make 'id' and 'name' fields clickable in the list view
    list_display_links = ('id', 'name',)
