from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin

from hub.models import LandTypeList


@admin.register(LandTypeList)
class LandTypeListAdmin(SimpleHistoryAdmin):
    pass
