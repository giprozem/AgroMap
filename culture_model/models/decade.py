from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Decade(models.Model):
    start_date = models.DateField(verbose_name=_('С'))
    end_date = models.DateField(verbose_name=_('До'))

    class Meta:
        verbose_name = _('Декада')
        verbose_name_plural = _('Декады')

    def __str__(self):
        return f"с {self.start_date} по {self.end_date}"
