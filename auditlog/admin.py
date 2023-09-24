# Import necessary modules and classes from Django and auditlog
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from auditlog.filters import CIDFilter, ResourceTypeFilter
from auditlog.mixins import LogEntryAdminMixin
from auditlog.models import LogEntry

# Register the LogEntry model in the admin interface
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin, LogEntryAdminMixin):
    # Define related fields to be selected in a single query
    list_select_related = ["content_type", "actor"]
    
    # Define the displayed columns in the admin list view
    list_display = [
        "created",
        "resource_url",
        "action",
        "user_url",
    ]

    # Define search fields for filtering
    search_fields = [
        "timestamp",
        "object_repr",
        "changes",
        "actor__first_name",
        "actor__last_name",
        f"actor__{get_user_model().USERNAME_FIELD}",
    ]
    
    # Define filters for the admin list view
    list_filter = ["action", ResourceTypeFilter, "actor"]
    
    # Define readonly fields in the admin view
    readonly_fields = ["created", "resource_url", "action", "user_url", "msg"]
    
    # Define fieldsets to organize fields in the admin form
    fieldsets = [
        (None, {"fields": ["created", "user_url", "resource_url", ]}),
        (_("Changes"), {"fields": ["action", "msg"]}),
    ]

    # Disable add, change, and delete permissions in the admin interface
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # Override the default queryset to include request information
    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request=request)
