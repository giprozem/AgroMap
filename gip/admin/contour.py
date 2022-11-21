from django.contrib.gis import admin

from gip.models import Contour


@admin.register(Contour)
class ContourAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')