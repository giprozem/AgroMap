from django.contrib.gis.db import models

from gip.models.base import BaseModel


class Region(BaseModel):
    name = models.CharField(max_length=55, verbose_name="Наименование области")
    population = models.IntegerField(verbose_name="Население")
    area = models.IntegerField(verbose_name="Площадь")
    density = models.FloatField(verbose_name="Плотность")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = "Области"
