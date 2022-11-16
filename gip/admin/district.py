from django.contrib.gis import admin

from gip.models import District


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass