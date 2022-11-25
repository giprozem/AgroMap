from django.contrib.gis import admin

from gip.models import CropYield


@admin.register(CropYield)
class CropYieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'year', 'contour']
    readonly_fields = ('created_at', 'updated_at')