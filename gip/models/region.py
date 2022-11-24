from django.contrib.gis.db import models

from gip.models.base import BaseModel


class Region(BaseModel):
    name = models.CharField(max_length=55)
    population = models.IntegerField()
    area = models.IntegerField()
    density = models.FloatField()

    def __str__(self):
        return self.name