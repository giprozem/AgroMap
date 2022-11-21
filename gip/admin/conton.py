from django.contrib.gis import admin

from gip.models import Conton


@admin.register(Conton)
class ContonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
