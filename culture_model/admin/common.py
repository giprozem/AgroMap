# Import necessary modules and classes
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin
from culture_model.models import Decade, VegetationIndex, IndexPlan, Phase

# Register the Decade model with the admin site using the DecadeAdmin class
@admin.register(Decade)
class DecadeAdmin(SimpleHistoryAdmin):
    pass

# Register the VegetationIndex model with the admin site using the IndexAdmin class
@admin.register(VegetationIndex)
class IndexAdmin(SimpleHistoryAdmin, TranslationAdmin):
    list_display = ('id', 'name')

# Register the IndexPlan model with the admin site using the IndexPlanAdmin class
@admin.register(IndexPlan)
class IndexPlanAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'value', 'culture', 'region']
    list_display_links = ['id', 'value']

# Register the Phase model with the admin site using the PhaseAdmin class
@admin.register(Phase)
class PhaseAdmin(SimpleHistoryAdmin, TranslationAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
