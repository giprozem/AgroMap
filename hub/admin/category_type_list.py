from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin

from hub.models import CategoryTypeList


@admin.register(CategoryTypeList)
class CategoryTypeListAdmin(SimpleHistoryAdmin):
    """
    This script provides an admin interface for managing `CategoryTypeList` model from the `hub` app using Django's admin
    site capabilities. It incorporates the `SimpleHistoryAdmin` to maintain a historical record of all changes made to
    each instance of `CategoryTypeList`.

    Class:
    - `CategoryTypeListAdmin`: This admin class inherits from `SimpleHistoryAdmin` to provide a user interface in Django's
      admin panel for CRUD operations on `CategoryTypeList` instances while also maintaining their change history.

    Attributes:
    - There aren't any attributes defined within the class, but the inheritance from `SimpleHistoryAdmin` brings in various
      features and functionalities specific to handling historical changes.

    Decorator:
    - `@admin.register(CategoryTypeList)`: This decorator registers the `CategoryTypeList` model with the Django admin
      site using the provided admin class `CategoryTypeListAdmin`. This ensures that when an admin user accesses the Django
      admin interface, they can view and manage the `CategoryTypeList` instances using the capabilities provided by
      `CategoryTypeListAdmin`.
    """
    pass
