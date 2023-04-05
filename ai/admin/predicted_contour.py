from django.contrib.admin import TabularInline
from django.contrib.gis import admin
from django.utils.safestring import mark_safe
from leaflet.admin import LeafletGeoAdmin

from ai.models import Contour_AI, Images_AI, Yolo, Dataset
from indexes.models import PredictedContourVegIndex
from django.utils.translation import gettext_lazy as _


class VegIndexTabularInline(TabularInline):
    model = PredictedContourVegIndex
    readonly_fields = ('id', 'get_html_photo', 'index_image', 'average_value', 'get_description', )
    fields = ('average_value', 'get_description', 'get_html_photo', 'index', 'contour', 'date', )
    show_change_link = ('index', )
    extra = 0

    def get_description(self, obj):
        return obj.meaning_of_average_value.description

    get_description.short_description = _("Значение индекса")

    def get_html_photo(self, obj):
        if obj.index_image:
            return mark_safe(f"<img src='{obj.index_image.url}' width=100>")

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    get_html_photo.short_description = _("Визуализация NDVI")


@admin.register(Contour_AI)
class Contour_AIAdmin(LeafletGeoAdmin):
    inlines = [VegIndexTabularInline]


@admin.register(Images_AI)
class Images_AIAdmin(admin.ModelAdmin):

    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=500>")


@admin.register(Yolo)
class YoloAdmin(admin.ModelAdmin):
    pass


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
