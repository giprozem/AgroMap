from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords

from gip.models.base import BaseModel
from gip.models.conton import Conton


class Village(BaseModel):
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='villages', verbose_name="Район")
    name = models.CharField(max_length=55, verbose_name="Село")
    polygon = models.MultiPolygonField(geography='Kyrgyzstan', verbose_name="Контур")
    history = HistoricalRecords()

    def __str__(self):
        return self.conton.name

    class Meta:
        verbose_name = 'Село'
        verbose_name_plural = "Сёла"
