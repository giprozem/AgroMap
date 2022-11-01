from django.contrib.gis import admin
from django.db import models
from plot.models import Plot, CultureField, Crop


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    pass


@admin.register(CultureField)
class CultureFieldAdmin(admin.OSMGeoAdmin):
    pass


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    pass