from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import Fertility


# @admin.register(Fertility)
# class FertilityAdmin(SimpleHistoryAdmin):
#     list_display = ('id', 'name', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('name', )
#     ordering = ('name', 'created_at', )
#     list_per_page = 20
#     search_fields = ('name', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'name', )
