from django.contrib.gis.db import models

from gip.models.base import BaseModel
from simple_history.models import HistoricalRecords


class Region(BaseModel):
    name = models.CharField(max_length=55, verbose_name="Наименование области")
    population = models.IntegerField(verbose_name="Население")
    area = models.IntegerField(verbose_name="Площадь")
    density = models.FloatField(verbose_name="Плотность")
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Контур", blank=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = "Области"
