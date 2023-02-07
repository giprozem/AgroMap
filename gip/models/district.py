from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.region import Region
from simple_history.models import HistoricalRecords


class District(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='Код СОАТО')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts', verbose_name="Область")
    name = models.CharField(max_length=55, verbose_name="Район")
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Контур")
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = "Район"
