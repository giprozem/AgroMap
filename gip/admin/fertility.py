from django.contrib.gis import admin

from gip.models import Fertility


@admin.register(Fertility)
class FertilityAdmin(admin.ModelAdmin):
    pass