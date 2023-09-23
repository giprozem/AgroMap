from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CultureModelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'culture_model'
    verbose_name = _('Cultures')