from django.contrib.admin.options import TabularInline
from django.contrib.gis import admin
from django.utils.safestring import mark_safe
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from gip.models import Contour, LandType, ContourYear
from indexes.models import ActualVegIndex


class NDVITabularInline(TabularInline):
    model = ActualVegIndex
    readonly_fields = ('id', 'get_html_photo', 'index_image', 'average_value', 'get_description', )
    fields = ('average_value', 'get_description', 'get_html_photo', 'index', 'contour', 'date', )
    show_change_link = ('index', )
    extra = 0

    def get_description(self, obj):
        return obj.meaning_of_average_value.description

    get_description.short_description = 'Index value'

    def get_html_photo(self, obj):
        if obj.index_image:
            return mark_safe(f"<img src='{obj.index_image.url}' width=100>")

    def get_static_png(self, obj):
        return mark_safe('''
        <div style="width: 290px;">
          <svg width="100%" height="50" viewBox="0 0 912 72" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="0" width="72" height="72" fill="rgb(0, 91, 76)"/>
          <rect x="72" width="72" height="72" fill="rgb(0, 112, 69)"/>
          <rect x="144" width="72" height="72" fill="rgb(0, 132, 54)"/>
          <rect x="216" width="72" height="72" fill="rgb(0, 151, 30)"/>
          <rect x="288" width="192" height="72" fill="#00AA00"/>
          <rect x="480" width="72" height="72" fill="rgb(60, 184, 34)"/>
          <rect x="552" width="72" height="72" fill="rgb(113, 197, 68)"/>
          <rect x="624" width="72" height="72" fill="rgb(160, 209, 102)"/>
          <rect x="696" width="72" height="72" fill="rgb(198, 221, 136)"/>
          <rect x="768" width="72" height="72" fill="rgb(227, 231, 170)"/>
          <rect x="840" width="72" height="72" fill="rgb(241, 237, 204)"/>
          </svg>
          <div style="display: flex; justify-content: space-between">
            <p style="margin: 0">high ndvi</p>
            <p style="margin: 0">low ndvi</p>
          </div>
        </div>
        ''')

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    get_html_photo.short_description = 'Visualization of NDVI'
    get_static_png.short_description = 'Vegetation index scale'


@admin.register(Contour)
class ContourAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_display = ('id', 'ink', 'code_soato', 'conton', 'farmer', )
    list_filter = ('conton', 'farmer', )
    ordering = ('conton', 'created_at')
    list_per_page = 20
    search_fields = ('conton__name', 'farmer__pin_inn', 'ink', )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'ink', )


@admin.register(ContourYear)
class ContourYearAdmin(LeafletGeoAdmin, SimpleHistoryAdmin, TranslationAdmin):
    readonly_fields = ('id', 'area_ha', 'code_soato', )
    list_display = ('id', 'code_soato', 'type', 'year', )
    list_filter = ('type', 'productivity', )
    ordering = ('id', )
    inlines = [NDVITabularInline]


@admin.register(LandType)
class LandTypeAdmin(TranslationAdmin):
    list_display = ('id', 'name' )
