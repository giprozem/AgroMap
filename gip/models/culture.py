from django.contrib.gis.db import models

from gip.models.base import BaseModel


class Culture(BaseModel):
    name = models.CharField(max_length=55)
    coefficient_crop = models.FloatField()

    def __str__(self):
        return self.name