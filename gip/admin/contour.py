from django.contrib.admin.options import TabularInline
from django.contrib.gis import admin
from django.utils.safestring import mark_safe
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import Contour
from indexes.models import NDVIIndex


class NDVITabularInline(TabularInline):
    model = NDVIIndex
    readonly_fields = ('id', 'get_html_photo', 'contour', 'date_of_satellite_image')
    fields = ('contour', 'date_of_satellite_image', 'ndvi_image', 'get_html_photo', )

    def get_html_photo(self, object):
        if object.ndvi_image:
            return mark_safe(f"<img src='{object.ndvi_image.url}' width=500>")

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    get_html_photo.short_description = 'Визуализация NDVI'


@admin.register(Contour)
class ContourAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at', 'sum_ha')
    list_display = ('id', 'ink', 'conton', 'farmer', )
    list_filter = ('conton', 'farmer', 'sum_ha', )
    ordering = ('conton', 'created_at')
    list_per_page = 20
    search_fields = ('conton__name', 'farmer__pin_inn', )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'ink', )
    inlines = [NDVITabularInline]
