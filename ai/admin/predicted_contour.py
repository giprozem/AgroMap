from django.contrib.gis import admin
from django.utils.safestring import mark_safe
from leaflet.admin import LeafletGeoAdmin

from ai.models import Contour_AI, Images_AI, Yolo


@admin.register(Contour_AI)
class Contour_AIAdmin(LeafletGeoAdmin):
    pass


@admin.register(Images_AI)
class Images_AIAdmin(admin.ModelAdmin):

    readonly_fields = ('get_html_photo',)
    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=500>")


@admin.register(Yolo)
class YoloAdmin(admin.ModelAdmin):
    pass