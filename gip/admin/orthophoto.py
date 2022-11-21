from django.contrib.gis import admin

from gip.models import OrthoPhoto


@admin.register(OrthoPhoto)
class OrthoPhotoAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')