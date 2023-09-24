from django.contrib.gis import admin  # Import Django's GIS admin module
from simple_history.admin import SimpleHistoryAdmin  # Import Simple History admin module

# Import the "DocumentTypeList" model from the "hub" app
from hub.models import DocumentTypeList

# Register the "DocumentTypeList" model with the Django admin site
@admin.register(DocumentTypeList)
class DocumentTypeListAdmin(SimpleHistoryAdmin):
    # Create an admin class for the "DocumentTypeList" model, based on SimpleHistoryAdmin
    pass  # Placeholder for any additional configurations you might want to add

