from django.contrib import admin
from culture_model.models.pasture_culture import Classes, Subclass, GroupType, RepublicanType, DistrictType, PastureCulture


@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


@admin.register(Subclass)
class SubclassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


@admin.register(GroupType)
class GroupTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(RepublicanType)
class RepublicanTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(DistrictType)
class DistrictTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(PastureCulture)
class PastureCultureAdmin(admin.ModelAdmin):
    pass
