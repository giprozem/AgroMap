from django.contrib.gis import admin

from gip.models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'population', 'area', 'density',  'created_by', 'updated_by', )
    readonly_fields = ('id', 'created_at', 'updated_at', )
    list_filter = ('name', 'population', 'area', 'density', )
    ordering = ('name', 'created_at', )
    list_per_page = 20
    search_fields = ('name', 'population', 'area', 'density', )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'name', )
