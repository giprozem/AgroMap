from django.contrib.gis import admin
from simple_history.admin import SimpleHistoryAdmin

from hub.models import DocumentTypeList


@admin.register(DocumentTypeList)
class DocumentTypeListAdmin(SimpleHistoryAdmin):
    pass
