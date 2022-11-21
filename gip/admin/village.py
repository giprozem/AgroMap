from django.contrib.gis import admin

from gip.models import Village


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
