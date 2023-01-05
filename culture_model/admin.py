from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from culture_model.models import Decade, Index, IndexPlan, Phase


@admin.register(Decade)
class DecadeAdmin(SimpleHistoryAdmin):
    pass


@admin.register(Index)
class IndexAdmin(SimpleHistoryAdmin):
    pass


@admin.register(IndexPlan)
class IndexPlanAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'value', 'culture', 'region']
    list_display_links = ['id', 'value']


@admin.register(Phase)
class PhaseAdmin(SimpleHistoryAdmin):
    pass

