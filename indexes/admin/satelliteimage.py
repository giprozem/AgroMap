from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.contrib.admin.widgets import AdminFileWidget
from django.db import models
from django.forms import FileInput
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from indexes.models.satelliteimage import SatelliteImages, SciHubAreaInterest, SciHubImageDate


@admin.register(SatelliteImages)
class SatelliteImagesAdmin(SimpleHistoryAdmin):
    readonly_fields = ('id', 'bbox', )


class SciHubImageDateInline(TabularInline):
    model = SciHubImageDate


class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None, renderer=None):
        output = []

        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)

            output.append(
                f' <a href="{image_url}" target="_blank">'
                f'  <img src="{image_url}" alt="{file_name}" width="150" height="150" '
                f'style="object-fit: cover;"/> </a>')

        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        from django.utils.safestring import mark_safe
        return mark_safe(u''.join(output))


# class SnapshotAdmin(admin.TabularInline):
#     model = Snapshot
#     fields = ('description', 'image', 'created_at')
#     max_num = 500
#     min_num = 1
#     extra = 0



@admin.register(SciHubAreaInterest)
class SciHubAreaInterestAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    inlines = [SciHubImageDateInline]


@admin.register(SciHubImageDate)
class SciHubImageDateAdmin(LeafletGeoAdmin, SimpleHistoryAdmin, admin.ModelAdmin):
    # formfield_overrides = {
    #     models.FileField: {'widget': FileInput}
    # }
    pass
