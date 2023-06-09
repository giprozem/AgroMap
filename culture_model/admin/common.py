from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from modeltranslation.admin import TranslationAdmin

from culture_model.models import Decade, VegetationIndex, IndexPlan, Phase


@admin.register(Decade)
class DecadeAdmin(SimpleHistoryAdmin):
    pass


@admin.register(VegetationIndex)
class IndexAdmin(SimpleHistoryAdmin, TranslationAdmin):
    list_display = ('id', 'name')


@admin.register(IndexPlan)
class IndexPlanAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'value', 'culture', 'region']
    list_display_links = ['id', 'value']


@admin.register(Phase)
class PhaseAdmin(SimpleHistoryAdmin, TranslationAdmin):
    pass

