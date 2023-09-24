# Import necessary modules and classes
from django.contrib import admin
from culture_model.models.pasture_culture import Classes, Subclass, GroupType, RepublicanType, DistrictType, PastureCulture

# Register the Classes model with the admin site using the ClassesAdmin class
@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

# Register the Subclass model with the admin site using the SubclassAdmin class
@admin.register(Subclass)
class SubclassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

# Register the GroupType model with the admin site using the GroupTypeAdmin class
@admin.register(GroupType)
class GroupTypeAdmin(admin.ModelAdmin):
    pass

# Register the RepublicanType model with the admin site using the RepublicanTypeAdmin class
@admin.register(RepublicanType)
class RepublicanTypeAdmin(admin.ModelAdmin):
    pass

# Register the DistrictType model with the admin site using the DistrictTypeAdmin class
@admin.register(DistrictType)
class DistrictTypeAdmin(admin.ModelAdmin):
    pass

# Register the PastureCulture model with the admin site using the PastureCultureAdmin class
@admin.register(PastureCulture)
class PastureCultureAdmin(admin.ModelAdmin):
    pass
