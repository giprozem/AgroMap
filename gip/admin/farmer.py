from django.contrib.gis import admin

from gip.models import Farmer


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    pass