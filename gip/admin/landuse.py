from django.contrib.admin import TabularInline
from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import LandUse, LandUsePhotos


# class LandUsePhotosAdmin(TabularInline):
#     model = LandUsePhotos
#     extra = 1
#
#
# @admin.register(LandUse)
# class LandUseAdmin(SimpleHistoryAdmin):
#     list_display = ('id', 'contour', 'farmer', 'culture', 'year', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('contour', 'farmer', 'culture', 'year', )
#     ordering = ('contour', 'created_at', )
#     list_per_page = 20
#     search_fields = ('contour__ink', 'farmer__pin_inn', 'culture__name', 'year', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'contour', )
#     inlines = [LandUsePhotosAdmin]



