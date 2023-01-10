from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin

from hub.models import PropertyTypeList


@admin.register(PropertyTypeList)
class PropertyTypeListAdmin(SimpleHistoryAdmin):
    pass
