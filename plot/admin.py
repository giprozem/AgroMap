from django.contrib import admin

from plot.models import Plot, Culture


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    pass


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    pass