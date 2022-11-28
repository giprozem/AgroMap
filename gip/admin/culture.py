from django.contrib.gis import admin

from gip.models import Culture


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'coefficient_crop', 'created_by', 'updated_by']
    readonly_fields = ('id', 'created_at', 'updated_at', )
    list_filter = ('name', 'coefficient_crop', )
    ordering = ('name', 'created_at')
    list_per_page = 20
    search_fields = ('name', 'coefficient_crop')
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'name', )
