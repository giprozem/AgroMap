from django.contrib.gis import admin

from ai.models.create_dataset import (
    Dataset,
    Process,
    Merge_Bands,
    Create_RGB,
    Cut_RGB_TIF,
    AI_Found,
    CreateDescription,
)


# Registering the Dataset model with read-only fields
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    # This admin class is used to manage Dataset objects.
    # It provides read-only fields for 'created_at' and 'updated_at' timestamps.


# Registering the Process model
@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    # This admin class is used to manage Process objects.
    # No specific customizations or restrictions are defined for this admin.
    pass


# Registering the Merge_Bands model
@admin.register(Merge_Bands)
class Merge_BandsAdmin(admin.ModelAdmin):
    # This admin class is used to manage Merge_Bands objects.
    # No specific customizations or restrictions are defined for this admin.
    pass


# Registering the Create_RGB model
@admin.register(Create_RGB)
class Create_RGBAdmin(admin.ModelAdmin):
    # This admin class is used to manage Create_RGB objects.
    # No specific customizations or restrictions are defined for this admin.
    pass


# Registering the Cut_RGB_TIF model
@admin.register(Cut_RGB_TIF)
class Cut_RGB_TIFAdmin(admin.ModelAdmin):
    # This admin class is used to manage Cut_RGB_TIF objects.
    # No specific customizations or restrictions are defined for this admin.
    pass


# Registering the AI_Found model
@admin.register(AI_Found)
class AI_FoundAdmin(admin.ModelAdmin):
    # This admin class is used to manage AI_Found objects.
    # No specific customizations or restrictions are defined for this admin.
    pass


# Registering the CreateDescription model
@admin.register(CreateDescription)
class CreateDescriptionAdmin(admin.ModelAdmin):
    # This admin class is used to manage CreateDescription objects.
    # No specific customizations or restrictions are defined for this admin.
    pass
