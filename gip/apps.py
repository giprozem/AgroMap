from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class GipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gip'
    verbose_name = _('AgroMap')

    def ready(self):
        # Import signals module when the app is ready.
        import gip.signals
