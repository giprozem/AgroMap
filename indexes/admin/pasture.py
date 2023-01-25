from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from indexes.models.pasture import ProductivityClass, ContourAverageIndex


@admin.register(ProductivityClass)
class ProductivityClassAdmin(SimpleHistoryAdmin):
    pass


@admin.register(ContourAverageIndex)
class ContourAverageIndex(SimpleHistoryAdmin):
    pass
