from django.contrib.gis import admin

from ai.models.create_dataset import Dataset, Process, Merge_Bands, Create_RGB, Cut_RGB_TIF, AI_Found, CreateDescription


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    pass


@admin.register(Merge_Bands)
class Merge_BandsAdmin(admin.ModelAdmin):
    pass


@admin.register(Create_RGB)
class Create_RGBAdmin(admin.ModelAdmin):
    pass


@admin.register(Cut_RGB_TIF)
class Cut_RGB_TIFAdmin(admin.ModelAdmin):
    pass


@admin.register(AI_Found)
class AI_FoundAdmin(admin.ModelAdmin):
    pass


@admin.register(CreateDescription)
class CreateDescriptionAdmin(admin.ModelAdmin):
    pass
