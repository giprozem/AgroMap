from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# Define an AppConfig for the "Culture Model" app
class CultureModelConfig(AppConfig):
    # Set the default primary key field type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Name of the app, should match the name of the app's directory
    name = 'culture_model'
    
    # Human-readable name for the app (used for display)
    verbose_name = _('Cultures')  # Translatable name using gettext_lazy
