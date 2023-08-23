from django.contrib.gis import admin
import json
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = (
        'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'action_time', 'message', )
    exclude = ('change_message', )
    list_filter = ('action_time', 'user',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def message(self, obj):
        return json.loads(obj.change_message)

    message.short_description = LogEntry._meta.get_field('change_message').verbose_name
