from django.contrib.gis.db import models

from gip.models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class Region(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_('Код СОАТО'))
    name = models.CharField(max_length=55, verbose_name=_('Область'))
    population = models.IntegerField(verbose_name=_('Население'))
    area = models.IntegerField(verbose_name=_('Площадь'))
    density = models.FloatField(verbose_name=_('Плотность'))
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_('Контур'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Область')
        verbose_name_plural = _('Области')
