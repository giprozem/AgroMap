from django.contrib.admin import TabularInline
from django.contrib.gis import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from leaflet.admin import LeafletGeoAdmin

from ai.models.predicted_contour import Contour_AI, Images_AI, Yolo
from indexes.models import PredictedContourVegIndex

# TabularInline for PredictedContourVegIndex
class VegIndexTabularInline(TabularInline):
    model = PredictedContourVegIndex
    readonly_fields = ('id', 'get_html_photo', 'index_image', 'average_value', 'get_description',)
    fields = ('average_value', 'get_description', 'get_html_photo', 'index', 'contour', 'date',)
    show_change_link = ('index',)
    extra = 0

    # Function to retrieve and display the description of the index value
    def get_description(self, obj):
        return obj.meaning_of_average_value.description

    get_description.short_description = _("Index Value")

    # Function to display an HTML-rendered photo
    def get_html_photo(self, obj):
        if obj.index_image:
            return mark_safe(f"<img src='{obj.index_image.url}' width=100>")

    # Permission functions to prevent changes and deletions in this inline
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    get_html_photo.short_description = _("NDVI Visualization")

# Admin registration for Contour_AI model with LeafletGeoAdmin
@admin.register(Contour_AI)
class Contour_AIAdmin(LeafletGeoAdmin):
    inlines = [VegIndexTabularInline]  # Include the VegIndexTabularInline as an inline
    list_display = ('id', 'district', 'culture', 'area_ha')
    list_filter = ('culture', 'district',)
    search_fields = ('district__name', 'district__region__name', 'id')

# Admin registration for Images_AI model
@admin.register(Images_AI)
class Images_AIAdmin(admin.ModelAdmin):
    readonly_fields = ('get_html_photo',)

    # Function to display an HTML-rendered photo
    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width=500>")

# Admin registration for Yolo model
@admin.register(Yolo)
class YoloAdmin(admin.ModelAdmin):
    pass
