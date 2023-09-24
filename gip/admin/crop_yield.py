# Import necessary modules
from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin
from leaflet.admin import LeafletGeoAdmin

from gip.models import CropYield

# Register the CropYield model with the admin panel
@admin.register(CropYield)
class CropYieldAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    # Define fields to be displayed in the list view
    list_display = ['id', 'culture', 'contour', 'year', 'season']
    
    # Define read-only fields
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    # Add filters for the 'culture', 'contour', 'year', and 'season' fields in the list view
    list_filter = ('culture', 'contour', 'year', 'season',)
    
    # Set the default ordering for the list view
    ordering = ('culture', 'created_at')
    
    # Specify the number of items displayed per page in the list view
    list_per_page = 20
    
    # Add search functionality for 'culture__name', 'contour__ink', 'year', and 'season' fields
    search_fields = ('culture__name', 'contour__ink', 'year', 'season',)
    
    # Add a date hierarchy based on the 'created_at' field
    date_hierarchy = 'created_at'
    
    # Make 'id' and 'culture' fields clickable in the list view
    list_display_links = ('id', 'culture',)
