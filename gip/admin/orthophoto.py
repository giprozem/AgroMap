from django.contrib.gis import admin

from gip.models import OrthoPhoto


@admin.register(OrthoPhoto)
class OrthoPhotoAdmin(admin.ModelAdmin):
    pass