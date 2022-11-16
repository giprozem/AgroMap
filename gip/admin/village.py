from django.contrib.gis import admin

from gip.models import Village


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    pass