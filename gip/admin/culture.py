# Import necessary modules
from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models import Culture

# Register the Culture model with the admin panel
@admin.register(Culture)
class CultureAdmin(SimpleHistoryAdmin, TranslationAdmin):
    # Define fields to be displayed in the list view
    list_display = ['id', 'name', 'coefficient_crop', ]
    
    # Define read-only fields
    readonly_fields = ('id', 'created_at', 'updated_at',)
    
    # Add filters for the 'name' and 'coefficient_crop' fields in the list view
    list_filter = ('name', 'coefficient_crop',)
    
    # Set the default ordering for the list view
    ordering = ('name', 'created_at')
    
    # Specify the number of items displayed per page in the list view
    list_per_page = 20
    
    # Add search functionality for 'name' and 'coefficient_crop' fields
    search_fields = ('name', 'coefficient_crop')
    
    # Add a date hierarchy based on the 'created_at' field
    date_hierarchy = 'created_at'
    
    # Make 'id' and 'name' fields clickable in the list view
    list_display_links = ('id', 'name',)
