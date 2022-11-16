from django.contrib.gis import admin

from gip.models import Culture


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    pass