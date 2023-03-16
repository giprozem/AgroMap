from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.region import Region
from django.utils.translation import gettext_lazy as _


class District(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_("Код СОАТО"))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts', verbose_name=_("Область"))
    name = models.CharField(max_length=55, verbose_name=_("Район"))
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Контур"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Район")
        verbose_name_plural = _("Районы")
