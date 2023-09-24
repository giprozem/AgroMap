from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IndexesConfig(AppConfig):
    """
    Configuration for the 'indexes' application. This is used by Django's application registry to configure
    various application settings and also for importing necessary signals for the app.
    """

    # The default field type for automatic primary key creation.
    default_auto_field = 'django.db.models.BigAutoField'

    # Unique name for the application. Used internally by Django.
    name = 'indexes'

    # A human-readable name for the application. Useful for admin interfaces.
    verbose_name = _('Vegetation indices')

    def ready(self):
        """
        Method to perform startup tasks. Here, it imports signals associated with the application.
        """
        import indexes.signals

