from django.contrib.gis.db import models

from gip.models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class SoilClass(BaseModel):
    ID = models.BigIntegerField(verbose_name='ID')
    name = models.CharField(max_length=255, verbose_name=_('Тип почвы'))
    description = models.TextField(verbose_name=_('Описание'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Тип почвы')
        verbose_name_plural = _('Типы почвы')


class SoilClassMap(BaseModel):
    soil_class = models.ForeignKey(SoilClass, on_delete=models.CASCADE, related_name='soil_class_maps',
                                   verbose_name=_('Тип почвы'))
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_('Контур'))

    class Meta:
        verbose_name = _('Контур типа почвы')
        verbose_name_plural = _('Контуры типа почвы')


class SoilProductivity(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Продуктивность почвы'))

    class Meta:
        verbose_name = _('Продуктивность почвы')
        verbose_name_plural = _('Продуктивность почв')


class SoilFertility(BaseModel):
    soil_productivity = models.ForeignKey(SoilProductivity, on_delete=models.CASCADE, related_name='soil_fertility',
                                          verbose_name=_('Плодородие почвы'))
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_('Контур'))

    class Meta:
        verbose_name = _('Плодородие почвы')
        verbose_name_plural = _('Плодородие почв')
