from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.region import Region


class District(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts', verbose_name="Область")
    name = models.CharField(max_length=55, verbose_name="Район")
    polygon = models.MultiPolygonField(geography='Kyrgyzstan', verbose_name="Контур")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = "Район"
