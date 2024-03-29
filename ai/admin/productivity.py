from django.contrib import admin
from django.utils.safestring import mark_safe
from ai.models.productivity import ProductivityML
from indexes.models import PredictedContourVegIndex, ContourAIIndexCreatingReport
from django.utils.translation import gettext_lazy as _

# Admin registration for ProductivityML model
@admin.register(ProductivityML)
class ProductivityMLAdmin(admin.ModelAdmin):
    pass

# Admin registration for PredictedContourVegIndex model
@admin.register(PredictedContourVegIndex)
class PredictedContourVegIndexAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'average_value', 'get_description', 'index', 'contour', 'date', 'get_html_photo', 'get_contour_id',)
    readonly_fields = (
        'id', 'average_value', 'get_html_photo', 'get_description', 'meaning_of_average_value', 'index_image')
    list_display_links = ('id', 'get_description',)
    list_filter = ('average_value', 'date', 'contour', 'meaning_of_average_value', 'id', 'index',)
    list_per_page = 20

    # Function to display an HTML-rendered photo
    def get_html_photo(self, obj):
        if obj.index_image:
            return mark_safe(f"<img src='{obj.index_image.url}' width=100>")

    get_html_photo.short_description = _('NDVI Visualization')

    # Function to retrieve the contour's ID
    def get_contour_id(self, obj):
        return obj.contour.id

    # Function to retrieve and display the description of the index value
    def get_description(self, obj):
        return obj.meaning_of_average_value.description if obj.meaning_of_average_value else None

    get_description.short_description = _('Index Value')

# Admin registration for ContourAIIndexCreatingReport model
@admin.register(ContourAIIndexCreatingReport)
class ContourAIIndexCreatingReportAdmin(admin.ModelAdmin):
    pass
