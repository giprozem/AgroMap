from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AuditlogConfig(AppConfig):
    # Name of the app
    name = "auditlog"

    # Verbose name for the app, used in the admin interface
    verbose_name = _("User Changes Report")

    # Define the default auto field for this app
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        # Import the auditlog registry and register models for auditing
        from auditlog.registry import auditlog
        auditlog.register_from_settings()

        # Import models from the auditlog app and set the 'changes_func' attribute
        from auditlog import models
        models.changes_func = models._changes_func()
