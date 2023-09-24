# Import necessary modules
from django.contrib.gis import admin
import json
from django.contrib.admin.models import LogEntry

# Register LogEntry model with admin panel
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # Define fields that should be read-only
    readonly_fields = (
        'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'action_time', 'message',
    )

    # Exclude 'change_message' field from the admin interface
    exclude = ('change_message', )

    # Define filters for the admin list view
    list_filter = ('action_time', 'user',)

    # Disable the add permission for LogEntry objects
    def has_add_permission(self, request, obj=None):
        return False

    # Disable the delete permission for LogEntry objects
    def has_delete_permission(self, request, obj=None):
        return False

    # Disable the change permission for LogEntry objects
    def has_change_permission(self, request, obj=None):
        return False

    # Define a custom method to display the 'message' field as JSON
    def message(self, obj):
        return json.loads(obj.change_message)

    # Set a user-friendly name for the 'message' method in the admin interface
    message.short_description = LogEntry._meta.get_field('change_message').verbose_name
