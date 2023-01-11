from django.contrib import admin
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from indexes.models import NDVIIndex, IndexFact, SatelliteImages, IndexMeaning
from indexes.forms import IndexMeaningForm


@admin.register(NDVIIndex)
class NDVIAdmin(SimpleHistoryAdmin):
    readonly_fields = ('id', 'get_html_photo', )
    fields = ('id', 'contour', 'date_of_satellite_image', 'ndvi_image', 'get_html_photo', 'average_NDVI', )
    list_display = ('id', 'contour', 'get_html_photo_to_main', )
    list_display_links = ('id', 'contour', 'get_html_photo_to_main', )

    def get_html_photo(self, object):
        if object.ndvi_image:
            return mark_safe(f"<img src='{object.ndvi_image.url}' width=500>")

    def get_html_photo_to_main(self, object):
        if object.ndvi_image:
            return mark_safe(f"<img src='{object.ndvi_image.url}' width=50>")

    get_html_photo.short_description = 'Фото NDVI'
    get_html_photo_to_main.short_description = 'Фото NDVI'


@admin.register(IndexFact)
class IndexFactAdmin(admin.ModelAdmin):
    list_display = ('id', 'average_value', 'get_description', 'decade', 'index', 'contour', 'source', 'get_html_photo', )
    readonly_fields = ('id', 'average_value', 'get_html_photo', )
    list_display_links = ('id', 'get_description', )

    def get_html_photo(self, object):
        if object.index_image:
            return mark_safe(f"<img src='{object.index_image.url}' width=100>")

    get_html_photo.short_description = 'Визуализация NDVI'

    def get_description(self, obj):
        return obj.meaning_of_average_value.description

    get_description.short_description = 'Значение показателя индекса'


@admin.register(SatelliteImages)
class SatelliteImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(IndexMeaning)
class IndexMeaningAdmin(admin.ModelAdmin):
    form = IndexMeaningForm
    # pass
