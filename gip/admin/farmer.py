from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin

from gip.models import Farmer


@admin.register(Farmer)
class FarmerAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'pin_inn', 'mobile']
    readonly_fields = ('id', 'created_at', 'updated_at', )
    list_filter = ('user', 'pin_inn', 'mobile', )
    ordering = ('user', 'created_at')
    list_per_page = 20
    search_fields = ('user', 'pin_inn', 'mobile')
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'user', )
