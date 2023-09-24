from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from indexes.models.pasture import ProductivityClass, ContourAverageIndex

"""
Register the ProductivityClass model in the Django Admin interface.
The SimpleHistoryAdmin mixin provides a historical view of the model's changes in the admin interface.
The TranslationAdmin mixin provides functionality to manage translated fields in the model.
"""


@admin.register(ProductivityClass)
class ProductivityClassAdmin(SimpleHistoryAdmin, TranslationAdmin):
    pass  # no custom behavior is defined for this model's admin representation


"""
Register the ContourAverageIndex model in the Django Admin interface.
The SimpleHistoryAdmin mixin provides a historical view of the model's changes in the admin interface.
"""


@admin.register(ContourAverageIndex)
class ContourAverageIndex(SimpleHistoryAdmin):
    readonly_fields = (
        'id', 'value', 'start_day', 'end_day', 'index_count')  # These fields are not editable in the admin form
    fields = ('id', 'contour', 'value', 'productivity_class', 'start_day', 'end_day',
              'index_count')  # Fields to be displayed in the model's edit form in the admin interface
    list_filter = (
        'contour', 'productivity_class', 'value',)  # Fields that can be used to filter the list view of the model
    list_display = (
        'id', 'contour',
        'get_contour_id')  # Fields to be displayed in the list view of the model in the admin interface

    # Define a custom method to display the ID of the related Contour object.
    # This can be useful for quick reference or lookup in the admin interface.
    def get_contour_id(self, obj):
        return obj.contour.id  # Return the ID of the related Contour object
