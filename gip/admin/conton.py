from django.contrib.gis import admin

from gip.models import Conton


@admin.register(Conton)
class ContonAdmin(admin.ModelAdmin):
    pass