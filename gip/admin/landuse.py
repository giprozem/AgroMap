from django.contrib.admin import TabularInline
from django.contrib.gis import admin

from gip.models import LandUse, LandUsePhotos


# class LandUsePhotosAdmin(TabularInline):
#     model = LandUsePhotos
#     extra = 1
#
#
# @admin.register(LandUse)
# class LandUseAdmin(admin.ModelAdmin):
#     list_display = ('id', 'contour', 'farmer', 'culture', 'year', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('contour', 'farmer', 'culture', 'year', )
#     ordering = ('contour', 'created_at', )
#     list_per_page = 20
#     search_fields = ('contour', 'farmer', 'culture', 'year', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'contour', )
#     inlines = [LandUsePhotosAdmin]



