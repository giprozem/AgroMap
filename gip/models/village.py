from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords

from gip.models.base import BaseModel
from gip.models.conton import Conton


class Village(BaseModel):
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='villages', verbose_name="Canton")
    name = models.CharField(max_length=55, verbose_name="Village")
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Polygon")
    # history = HistoricalRecords()

    def __str__(self):
        return self.conton.name

    class Meta:
        verbose_name = 'Village'
        verbose_name_plural = "Villages"
