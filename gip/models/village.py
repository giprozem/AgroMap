from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from gip.models.base import BaseModel
from gip.models.conton import Conton


class Village(BaseModel):
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='villages', verbose_name=_('Округ'))
    name = models.CharField(max_length=55, verbose_name=_('Село'))
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_('Контур'))

    def __str__(self):
        return self.conton.name

    class Meta:
        verbose_name = _('Село')
        verbose_name_plural = _('Сёла')
