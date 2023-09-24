from django.contrib.gis import admin  # Import Django's GIS admin module
from leaflet.admin import LeafletGeoAdmin  # Import Leaflet Geo admin module
from simple_history.admin import SimpleHistoryAdmin  # Import Simple History admin module

# Import the "LandInfo" model from the "hub" app
from hub.models import LandInfo

# Register the "LandInfo" model with the Django admin site
@admin.register(LandInfo)
class LandInfoAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    # Create an admin class for the "LandInfo" model, based on LeafletGeoAdmin and SimpleHistoryAdmin

    # Define the list of fields to display in the admin list view
    list_display = ['id', 'ink_code']
