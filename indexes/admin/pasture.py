from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from indexes.models.pasture import ProductivityClass, ContourAverageIndex


@admin.register(ProductivityClass)
class ProductivityClassAdmin(SimpleHistoryAdmin, TranslationAdmin):
    pass


@admin.register(ContourAverageIndex)
class ContourAverageIndex(SimpleHistoryAdmin):
    readonly_fields = ('id', 'value', 'start_day', 'end_day', 'index_count')
    fields = ('id', 'contour', 'value', 'productivity_class', 'start_day', 'end_day', 'index_count')
    list_filter = ('contour', 'productivity_class', 'value',)
    list_display = ('id', 'contour', 'get_contour_id')

    def get_contour_id(self, obj):
        return obj.contour.id
