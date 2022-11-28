from django.contrib.gis import admin

from gip.models import Fertility


# @admin.register(Fertility)
# class FertilityAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'created_by', 'updated_by', )
#     readonly_fields = ('id', 'created_at', 'updated_at', )
#     list_filter = ('name', )
#     ordering = ('name', 'created_at', )
#     list_per_page = 20
#     search_fields = ('name', )
#     date_hierarchy = 'created_at'
#     list_display_links = ('id', 'name', )
