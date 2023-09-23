from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.district import District
from django.utils.translation import gettext_lazy as _


class Conton(BaseModel):
    code_soato_vet = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_('Veterinary SOATO Code'))
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_("SOATO Code"))
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='contons', verbose_name=_("District"))
    name = models.CharField(max_length=55, verbose_name=_("District Name"))
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Contour"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
