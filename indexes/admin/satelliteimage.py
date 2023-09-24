import rasterio
from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.contrib.gis.geos import Polygon
from leaflet.admin import LeafletGeoAdmin
from rasterio import warp
from simple_history.admin import SimpleHistoryAdmin

from indexes.models.satelliteimage import SciHubAreaInterest, SciHubImageDate


# Inline model for SciHubImageDate to be displayed within the parent model (SciHubAreaInterest) in the admin interface.
class SciHubImageDateInline(TabularInline):
    model = SciHubImageDate


# Custom widget to display images in the Django admin form.
class AdminImageWidget(AdminFileWidget):

    def render(self, name, value, attrs=None, renderer=None):
        output = []

        # If there's an image, generate its preview.
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)

            output.append(
                f' <a href="{image_url}" target="_blank">'
                f'  <img src="{image_url}" alt="{file_name}" width="150" height="150" '
                f'style="object-fit: cover;"/> </a>')

        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))


# Django admin representation of SciHubAreaInterest model.
@admin.register(SciHubAreaInterest)
class SciHubAreaInterestAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    inlines = [SciHubImageDateInline]  # Includes SciHubImageDate as inline.


# Django admin representation of SciHubImageDate model.
@admin.register(SciHubImageDate)
class SciHubImageDateAdmin(LeafletGeoAdmin, SimpleHistoryAdmin, admin.ModelAdmin):
    list_display = ('id', 'date', 'area_interest', 'created_at', 'note', 'no_image')  # Fields to display in list view.
    list_display_links = ('id', 'date', 'area_interest')  # Fields to use as clickable links to detailed view.
    search_fields = ('name_product',)  # Fields to use in search bar.
    list_filter = ('area_interest', 'date')  # Fields to use as filters.
    readonly_fields = ('get_html_photo',)  # Non-editable fields.

    # Method to display a thumbnail of the image in the admin interface.
    def get_html_photo(self, obj):
        if obj.image_png:
            return mark_safe(f"<img src='{obj.image_png.url}'")

    # Overriding the save method to calculate and store the bounding box of the raster image when the record is saved.
    def save_model(self, request, obj, form, change):
        if obj.B01:
            # Open the raster file using rasterio.
            with rasterio.open(obj.B01) as src:
                bbox_m = src.bounds  # Get bounding box in the source coordinate reference system.
                # Transform bounding box to EPSG:4326.
                bbox = warp.transform_bounds(src.crs, {'init': 'EPSG:4326'}, *bbox_m)
                # Convert bounding box to a polygon.
                bboxs = Polygon.from_bbox(bbox)
                obj.polygon = bboxs  # Assign polygon to model's polygon field.
        obj.save()  # Save the model instance.
