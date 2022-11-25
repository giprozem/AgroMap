from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.district import District
from simple_history.models import HistoricalRecords


class Conton(BaseModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='contons')
    name = models.CharField(max_length=55)
    polygon = models.MultiPolygonField(geography='Kyrgyzstan')
    history = HistoricalRecords()

    def __str__(self):
        return self.name
