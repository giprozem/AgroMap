from django.contrib import admin
from django.utils.safestring import mark_safe

from indexes.admin.forms import IndexMeaningForm
from indexes.models import IndexFact, IndexMeaning


@admin.register(IndexFact)
class IndexFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'average_value', 'get_description', 'index', 'contour', 'source', 'get_html_photo', )
    readonly_fields = ('id', 'average_value', 'get_html_photo', )
    list_display_links = ('id', 'get_description', )

    def get_html_photo(self, object):
        if object.index_image:
            return mark_safe(f"<img src='{object.index_image.url}' width=100>")

    get_html_photo.short_description = 'Визуализация NDVI'

    def get_description(self, obj):
        return obj.meaning_of_average_value.description

    get_description.short_description = 'Значение показателя индекса'


@admin.register(IndexMeaning)
class IndexMeaningAdmin(admin.ModelAdmin):
    form = IndexMeaningForm
