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
    pass


@admin.register(Phase)
class PhaseAdmin(SimpleHistoryAdmin):
    pass

