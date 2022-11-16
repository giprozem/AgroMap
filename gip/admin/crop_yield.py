from django.contrib.gis import admin

from gip.models import CropYield


@admin.register(CropYield)
class CropYieldAdmin(admin.ModelAdmin):
    pass