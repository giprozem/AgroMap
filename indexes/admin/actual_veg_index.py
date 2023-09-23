from django.contrib import admin
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _

from indexes.admin.forms import IndexMeaningForm
from indexes.models import ActualVegIndex, IndexMeaning
from indexes.models.actual_veg_index_logs import IndexCreatingReport

@admin.register(ActualVegIndex)
class IndexFactAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'average_value', 'get_description', 'index', 'contour', 'date', 'get_html_photo')
    readonly_fields = (
    'id', 'average_value', 'get_html_photo', 'get_description', 'meaning_of_average_value', 'index_image')
    list_display_links = ('id', 'get_description', 'contour')
    list_filter = ('average_value', 'date', 'contour', 'meaning_of_average_value', 'contour__id',)
    list_per_page = 20

    def get_html_photo(self, obj):
        if obj.index_image:
            return mark_safe(f"<img src='{obj.index_image.url}' width=100>")

    get_html_photo.short_description = _('NDVI Visualization')

    def get_contour_id(self, obj):
        return obj.contour.id

    def get_description(self, obj):
        return obj.meaning_of_average_value.description if obj.meaning_of_average_value else None

    get_description.short_description = _('Index Value')

@admin.register(IndexMeaning)
class IndexMeaningAdmin(TranslationAdmin):
    form = IndexMeaningForm
    list_filter = ('index',)
    list_display = ('id', 'index', 'min_index_value', 'max_index_value',)
    list_display_links = ('id', 'index')

@admin.register(IndexCreatingReport)
class IndexCreatingReportAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'contour', 'veg_index', 'satellite_image', 'is_processed', 'process_error',)
    list_display = ('id', 'contour', 'veg_index', 'is_processed', 'process_error',)
    list_display_links = ('id', 'contour',)
    list_filter = ('contour', 'veg_index', 'satellite_image', 'is_processed', 'process_error', 'contour__id',)
    list_per_page = 20
