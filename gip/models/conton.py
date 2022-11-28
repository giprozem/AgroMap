from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.district import District
from simple_history.models import HistoricalRecords


class Conton(BaseModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='contons', verbose_name='Район')
    name = models.CharField(max_length=55, verbose_name="Наименование Айылного аймака")
    polygon = models.MultiPolygonField(geography='Kyrgyzstan', verbose_name="Контур")
    history = HistoricalRecords(verbose_name="История")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Айыл Аймак'
        verbose_name_plural = "Айылные Аймаки"
