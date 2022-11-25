from django.contrib.gis import admin

from gip.models import Culture


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'coefficient_crop']
    readonly_fields = ('created_at', 'updated_at')