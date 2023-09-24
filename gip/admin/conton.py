# Import necessary modules
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models import Conton

# Register the Conton model with the admin panel
@admin.register(Conton)
class ContonAdmin(LeafletGeoAdmin, SimpleHistoryAdmin, TranslationAdmin):
    # Define read-only fields
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    # Define fields to be displayed in the list view
    list_display = ('id', 'name', 'district',)
    
    # Add filters for the 'name' and 'district' fields in the list view
    list_filter = ('name', 'district',)
    
    # Set the default ordering for the list view
    ordering = ('name', 'created_at')
    
    # Specify the number of items displayed per page in the list view
    list_per_page = 20
    
    # Add search functionality for 'name' and 'district__name' fields
    search_fields = ('name', 'district__name',)
    
    # Add a date hierarchy based on the 'created_at' field
    date_hierarchy = 'created_at'
    
    # Make 'id' and 'name' fields clickable in the list view
    list_display_links = ('id', 'name',)
