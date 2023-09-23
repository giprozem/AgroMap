from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hub'
    verbose_name = _('Giprozem reference database')
