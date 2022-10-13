from django.contrib import admin
from django.db import models
from plot.models import Plot, Culture


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    pass

    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = [
    #         [
    #             None,
    #             {"fields": ["user", "name", "region"]},
    #         ],
    #         ["Geographic information", {"fields": ["geometry", "_area"]}],
    #     ]
    #     # if obj:
    #     #     fieldsets += ["Statistics", {"fields": ["_area"]}]
    #     return fieldsets
    #
    # def get_readonly_fields(self, request, obj):
    #     readonly_fields = super().get_readonly_fields(request, obj)
    #     readonly_fields += ("id", "_area")
    #     return readonly_fields
    #
    # def _area(self, obj):
    #     if obj.area is not None and obj.area > 0:
    #         if obj.area < 10000:
    #             return f"{round(obj.area, 0)} m2"
    #         return f"{round(obj.area / 10000, 2)} ha"
    #     return "-"
    # _area.short_description = "area"


@admin.register(Culture)
class CultureAdmin(admin.ModelAdmin):
    pass