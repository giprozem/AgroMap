from django.contrib.gis import admin

from gip.models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass