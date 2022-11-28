from django.contrib.gis import admin

from gip.models import OrthoPhoto


@admin.register(OrthoPhoto)
class OrthoPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'layer_name', 'use_y_n', 'url',  'created_by', 'updated_by', )
    readonly_fields = ('id', 'created_at', 'updated_at', )
    list_filter = ('layer_name', 'use_y_n', )
    ordering = ('layer_name', 'created_at', )
    list_per_page = 20
    search_fields = ('layer_name', )
    date_hierarchy = 'created_at'
    list_display_links = ('id', 'layer_name', )
