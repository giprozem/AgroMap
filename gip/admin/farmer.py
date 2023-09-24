# Import necessary modules
from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import Farmer

# Register the Farmer model with the admin panel
@admin.register(Farmer)
class FarmerAdmin(SimpleHistoryAdmin):
    # Define fields to be displayed in the list view
    list_display = ['id', 'user', 'pin_inn', 'mobile']
    
    # Define read-only fields
    readonly_fields = ('id', 'created_at', 'updated_at',)
    
    # Add filters for the 'user', 'pin_inn', and 'mobile' fields in the list view
    list_filter = ('user', 'pin_inn', 'mobile',)
    
    # Set the default ordering for the list view
    ordering = ('user', 'created_at')
    
    # Specify the number of items displayed per page in the list view
    list_per_page = 20
    
    # Add search functionality for 'user__username', 'pin_inn', and 'mobile' fields
    search_fields = ('user__username', 'pin_inn', 'mobile')
    
    # Add a date hierarchy based on the 'created_at' field
    date_hierarchy = 'created_at'
    
    # Make 'id' and 'user' fields clickable in the list view
    list_display_links = ('id', 'user',)
