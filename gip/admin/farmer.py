from django.contrib.gis import admin

from gip.models import Farmer


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['id', 'pin_inn', 'mobile']
    readonly_fields = ('created_at', 'updated_at')