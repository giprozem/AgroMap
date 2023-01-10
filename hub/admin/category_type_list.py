from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin

from hub.models import CategoryTypeList


@admin.register(CategoryTypeList)
class CategoryTypeListAdmin(SimpleHistoryAdmin):
    pass
