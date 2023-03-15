from django.contrib.gis import admin
from django.utils.safestring import mark_safe

from container.models import ImageBin


@admin.register(ImageBin)
class ImageBinTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'get_html_photo', )
    fields = ('id', 'id_image', 'image', 'get_html_photo', 'object_quantity', 'percent',)

    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=500>")
