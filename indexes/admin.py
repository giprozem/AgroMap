from django.contrib import admin
from django.utils.safestring import mark_safe

from indexes.models import NDVIIndex


@admin.register(NDVIIndex)
class NDVIAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'get_html_photo', )
    fields = ('id', 'coordinates', 'ndvi_image', 'get_html_photo', )
    list_display = ('id', 'get_html_photo_to_main', 'coordinates', )
    list_display_links = ('id', 'coordinates', 'get_html_photo_to_main', )

    def get_html_photo(self, object):
        if object.ndvi_image:
            return mark_safe(f"<img src='{object.ndvi_image.url}' width=500>")

    def get_html_photo_to_main(self, object):
        if object.ndvi_image:
            return mark_safe(f"<img src='{object.ndvi_image.url}' width=50>")

    get_html_photo.short_description = 'Фото NDVI'
    get_html_photo_to_main.short_description = 'Фото NDVI'
