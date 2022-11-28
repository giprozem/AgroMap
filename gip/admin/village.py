from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import Village


# @admin.register(Village)
# class VillageAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
#     list_display = ('id', 'name', 'conton', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('name', 'conton', )
#     ordering = ('name', 'created_at', )
#     list_per_page = 20
#     search_fields = ('name', 'conton', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'name', )
