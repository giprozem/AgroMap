# Import necessary modules
from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models import District
from leaflet.admin import LeafletGeoAdmin

# Register the District model with the admin panel
@admin.register(District)
class DistrictAdmin(LeafletGeoAdmin, SimpleHistoryAdmin, TranslationAdmin):
    # Define fields to be displayed in the list view
    list_display = ['id', 'name', 'region']
    
    # Define read-only fields
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    # Add filters for the 'region' and 'name' fields in the list view
    list_filter = ('region', 'name',)
    
    # Set the default ordering for the list view
    ordering = ('name', 'created_at')
    
    # Specify the number of items displayed per page in the list view
    list_per_page = 20
    
    # Add search functionality for 'name' and 'region__name' fields
    search_fields = ('name', 'region__name')
    
    # Add a date hierarchy based on the 'created_at' field
    date_hierarchy = 'created_at'
    
    # Make 'id' and 'name' fields clickable in the list view
    list_display_links = ('id', 'name',)
