from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class VegetationIndex(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'))

    class Meta:
        verbose_name = _('Индекс')
        verbose_name_plural = _('Индексы')

    def __str__(self):
        return self.name
