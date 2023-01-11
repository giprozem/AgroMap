from django.contrib import admin
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from indexes.models.ndvi import NDVIIndex


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
