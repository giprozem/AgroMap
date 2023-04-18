from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from indexes.models.satelliteimage import SciHubAreaInterest, SciHubImageDate


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
    list_display = ('id', 'date', 'area_interest', 'no_image')
    list_display_links = ('id', 'date', 'area_interest')
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, obj):
        if obj.image_png:
            return mark_safe(f"<img src='{obj.image_png.url}' width=710, height=600>")
