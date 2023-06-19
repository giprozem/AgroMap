from django.contrib.gis import admin

from django.contrib.admin.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = (
        'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message', 'action_time',)
    list_filter = ('action_time', 'user',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
