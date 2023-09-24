# Import necessary modules
from django.contrib.admin.options import TabularInline
from django.contrib.gis import admin
from django.utils.safestring import mark_safe
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _

from gip.models import Contour, LandType, Elevation
from indexes.models import ActualVegIndex

# Define an inline admin class for ActualVegIndex
class ActualVegIndexTabularInline(TabularInline):
    model = ActualVegIndex
    readonly_fields = ('id', 'get_html_photo', 'index_image', 'average_value', 'get_description',)
    fields = ('average_value', 'get_description', 'get_html_photo', 'index', 'contour', 'date',)
    show_change_link = ('index',)
    extra = 0

    # Define a custom method to display the description for 'average_value'
    def get_description(self, obj):
        return obj.meaning_of_average_value.description

    get_description.short_description = _("Index Value")

    # Define a custom method to display an HTML photo using 'index_image'
    def get_html_photo(self, obj):
        if obj.index_image:
            return mark_safe(f"<img src='{obj.index_image.url}' width=100>")

    # Override permission to change ActualVegIndex objects
    def has_change_permission(self, request, obj=None):
        return False

    # Override permission to delete ActualVegIndex objects
    def has_delete_permission(self, request, obj=None):
        return False

    get_html_photo.short_description = _("NDVI Visualization")

# Register the Contour model with the admin panel
@admin.register(Contour)
class ContourAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at', 'elevation', 'area_ha', 'soil_class')
    list_display = ('id', 'ink', 'code_soato', 'conton', 'display_district_name', 'elevation')
    list_filter = ('conton', 'farmer', 'id', 'type', 'culture')
    ordering = ('conton', 'created_at')
    list_per_page = 20
    search_fields = ('conton__name', 'farmer__pin_inn', 'ink', 'id', 'conton__district__name_ru')
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'ink',)
    inlines = [ActualVegIndexTabularInline]

    # Define a custom method to display the district name
    def display_district_name(self, obj):
        return obj.conton.district

    display_district_name.short_description = 'District'

# Register the LandType model with the admin panel
@admin.register(LandType)
class LandTypeAdmin(TranslationAdmin):
    list_display = ('id', 'name')

# Register the Elevation model with the admin panel
@admin.register(Elevation)
class ElevationAdmin(admin.ModelAdmin):
    pass
