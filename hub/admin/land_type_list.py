from django.contrib.gis import admin  # Import Django's GIS admin module
from simple_history.admin import SimpleHistoryAdmin  # Import Simple History admin module

# Import the "LandTypeList" model from the "hub" app
from hub.models import LandTypeList

# Register the "LandTypeList" model with the Django admin site
@admin.register(LandTypeList)
class LandTypeListAdmin(SimpleHistoryAdmin):
    # Create an admin class for the "LandTypeList" model, based on SimpleHistoryAdmin
    pass  # Placeholder for any additional configurations you might want to add
