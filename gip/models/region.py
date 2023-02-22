from django.contrib.gis.db import models

from gip.models.base import BaseModel
from simple_history.models import HistoricalRecords


class Region(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='SOATO code')
    name = models.CharField(max_length=55, verbose_name="Region name")
    population = models.IntegerField(verbose_name="Population")
    area = models.IntegerField(verbose_name="Area")
    density = models.FloatField(verbose_name="density")
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Polygon", blank=True, null=True)
    history = HistoricalRecords(excluded_fields=['name_ru', 'name_en', 'name_ky'])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = "Regions"
