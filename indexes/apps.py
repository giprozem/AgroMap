from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IndexesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indexes'
    verbose_name = _('Вегатационные индексы')

    def ready(self):
        import indexes.signals
