from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from gip.models import Village


# @admin.register(Village)
# class VillageAdmin(LeafletGeoAdmin):
#     list_display = ('id', 'name', 'conton', 'created_by', 'updated_by', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('name', 'conton', )
#     ordering = ('name', 'created_at', )
#     list_per_page = 20
#     search_fields = ('name', 'conton', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'name', )
