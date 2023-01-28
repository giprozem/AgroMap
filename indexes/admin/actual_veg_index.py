from django.contrib import admin
from django.utils.safestring import mark_safe

from indexes.admin.forms import IndexMeaningForm
from indexes.models import ActuaVegIndex, IndexMeaning
from simple_history.admin import SimpleHistoryAdmin


@admin.register(ActuaVegIndex)
class IndexFactAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'average_value', 'get_description', 'index', 'contour', 'date', 'get_html_photo', 'get_contour_id', )
    readonly_fields = ('id', 'average_value', 'get_html_photo', 'get_description', 'meaning_of_average_value', 'index_image')
    list_display_links = ('id', 'get_description', )
    list_filter = ('average_value', 'date', 'contour')

    def get_html_photo(self, obj):
        if obj.index_image:
            return mark_safe(f"<img src='{obj.index_image.url}' width=100>")

    get_html_photo.short_description = 'Визуализация NDVI'

    def get_contour_id(self, obj):
        return obj.contour.id

    def get_description(self, obj):
        return obj.meaning_of_average_value.description if obj.meaning_of_average_value else None

    get_description.short_description = 'Значение показателя индекса'


@admin.register(IndexMeaning)
class IndexMeaningAdmin(admin.ModelAdmin):
    form = IndexMeaningForm
    list_filter = ('index', )
    list_display = ('id', 'index', 'min_index_value', 'max_index_value', )
    list_display_links = ('id', 'index')
