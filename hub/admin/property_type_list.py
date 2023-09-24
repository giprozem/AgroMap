from django.contrib.gis import admin  # Import Django's GIS admin module
from simple_history.admin import SimpleHistoryAdmin  # Import Simple History admin module

# Import the "PropertyTypeList" model from the "hub" app
from hub.models import PropertyTypeList

# Register the "PropertyTypeList" model with the Django admin site
@admin.register(PropertyTypeList)
class PropertyTypeListAdmin(SimpleHistoryAdmin):
    # Create an admin class for the "PropertyTypeList" model, based on SimpleHistoryAdmin
    pass  # Placeholder for any additional configurations you might want to add
