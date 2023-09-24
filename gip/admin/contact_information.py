# Import necessary modules
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models import Department, ContactInformation

# Register the Department model with the admin panel
@admin.register(Department)
class DepartmentAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    # Define read-only fields
    readonly_fields = ('id',)
    
    # Define fields to be displayed in the list view
    list_display = ('id', 'name')
    
    # Add a filter for the 'name' field in the list view
    list_filter = ('name',)
    
    # Set the default ordering for the list view
    ordering = ('name',)
    
    # Add search functionality for the 'name' field
    search_fields = ('name',)
    
    # Make 'id' and 'name' fields clickable in the list view
    list_display_links = ('id', 'name')

# Register the ContactInformation model with the admin panel
@admin.register(ContactInformation)
class ContactInformationAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    # Define read-only fields
    readonly_fields = ('id', )
    
    # Define fields to be displayed in the list view
    list_display = ('id', 'title', 'fullname')
    
    # Add a filter for the 'title' field in the list view
    list_filter = ('title',)
    
    # Set the default ordering for the list view
    ordering = ('title',)
    
    # Add search functionality for 'title', 'department__name', and 'fullname' fields
    search_fields = ('title', 'department__name', 'fullname')
    
    # Make 'id' and 'title' fields clickable in the list view
    list_display_links = ('id', 'title')
