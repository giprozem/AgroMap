from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.district import District
from django.utils.translation import gettext_lazy as _


class Conton(BaseModel):
    code_soato_vet = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_('Код СОАТО ВЕТ'))
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_("Код СОАТО"))
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='contons', verbose_name=_("Район"))
    name = models.CharField(max_length=55, verbose_name=_("Округ"))
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Контур"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Округ")
        verbose_name_plural = _("Округи")
