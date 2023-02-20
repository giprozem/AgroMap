from django.contrib import admin
from django.contrib.admin.options import TabularInline
from leaflet.admin import LeafletGeoAdmin
from simple_history.admin import SimpleHistoryAdmin

from indexes.models.satelliteimage import SatelliteImages, SciHubAreaInterest, SciHubImageDate


@admin.register(SatelliteImages)
class SatelliteImagesAdmin(SimpleHistoryAdmin):
    readonly_fields = ('id', 'bbox', )


class SciHubImageDateInline(TabularInline):
    model = SciHubImageDate


@admin.register(SciHubAreaInterest)
class SciHubAreaInterestAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    inlines = [SciHubImageDateInline]


@admin.register(SciHubImageDate)
class SciHubImageDateAdmin(LeafletGeoAdmin, SimpleHistoryAdmin):
    pass
