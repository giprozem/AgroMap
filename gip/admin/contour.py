from django.contrib.gis import admin

from gip.models import Contour


@admin.register(Contour)
class ContourAdmin(admin.ModelAdmin):
    pass