from django.contrib import admin
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _

from indexes.admin.forms import IndexMeaningForm
from indexes.models import ActualVegIndex, IndexMeaning
from indexes.models.actual_veg_index_logs import IndexCreatingReport


# Custom Admin interface for the ActualVegIndex model
@admin.register(ActualVegIndex)
class IndexFactAdmin(SimpleHistoryAdmin):
    # Display these fields in the admin list view
    list_display = ('id', 'average_value', 'get_description', 'index', 'contour', 'date', 'get_html_photo')
    # Make these fields readonly
    readonly_fields = (
        'id', 'average_value', 'get_html_photo', 'get_description', 'meaning_of_average_value', 'index_image'
    )
    # Fields that can be clicked to navigate to the detail view
    list_display_links = ('id', 'get_description', 'contour')
    # Fields to add to the filter sidebar
    list_filter = ('average_value', 'date', 'contour', 'meaning_of_average_value', 'contour__id',)
    # Number of items per page
    list_per_page = 20

    # Method to display an image in the admin list view
    def get_html_photo(self, obj):
        if obj.index_image:
            return mark_safe(f"<img src='{obj.index_image.url}' width=100>")

    get_html_photo.short_description = _('NDVI Visualization')

    # Method to return the description of the associated IndexMeaning
    def get_description(self, obj):
        return obj.meaning_of_average_value.description if obj.meaning_of_average_value else None

    get_description.short_description = _('Index Value')


# Custom Admin interface for the IndexMeaning model with translation support
@admin.register(IndexMeaning)
class IndexMeaningAdmin(TranslationAdmin):
    form = IndexMeaningForm  # Use the custom IndexMeaningForm for editing
    list_filter = ('index',)
    list_display = ('id', 'index', 'min_index_value', 'max_index_value',)
    list_display_links = ('id', 'index')


# Custom Admin interface for the IndexCreatingReport model
@admin.register(IndexCreatingReport)
class IndexCreatingReportAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'contour', 'veg_index', 'satellite_image', 'is_processed', 'process_error',)
    list_display = ('id', 'contour', 'veg_index', 'is_processed', 'process_error',)
    list_display_links = ('id', 'contour',)
    list_filter = ('contour', 'veg_index', 'satellite_image', 'is_processed', 'process_error', 'contour__id',)
    list_per_page = 20
