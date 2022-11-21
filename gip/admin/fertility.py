from django.contrib.gis import admin

from gip.models import Fertility


@admin.register(Fertility)
class FertilityAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')