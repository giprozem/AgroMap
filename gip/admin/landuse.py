from django.contrib.gis import admin

from gip.models import LandUse


@admin.register(LandUse)
class LandUseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')