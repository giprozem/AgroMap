from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from indexes.models.pasture import ProductivityClass, ContourAverageIndex


@admin.register(ProductivityClass)
class ProductivityClassAdmin(SimpleHistoryAdmin):
    pass


@admin.register(ContourAverageIndex)
class ContourAverageIndex(SimpleHistoryAdmin):
    readonly_fields = ('id', 'value', 'start_day', 'end_day', 'index_count')
    fields = ('id', 'contour', 'value', 'productivity_class', 'start_day', 'end_day', 'index_count')
    list_filter = ('contour', 'productivity_class', 'value', 'contour__is_rounded')
