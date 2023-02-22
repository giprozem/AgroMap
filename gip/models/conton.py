from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.district import District
from simple_history.models import HistoricalRecords


class Conton(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='SOATO code')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='contons', verbose_name='District')
    name = models.CharField(max_length=55, verbose_name="Aiyl aimag name")
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Polygon", blank=True, null=True)
    history = HistoricalRecords(verbose_name="History")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aiyl aimag'
        verbose_name_plural = "Aiyl aimags"
