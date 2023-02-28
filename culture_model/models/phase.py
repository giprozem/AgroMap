from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Phase(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('Название'))

    class Meta:
        verbose_name = _('Фаза развития')
        verbose_name_plural = _('Фазы развития')

    def __str__(self):
        return self.name
