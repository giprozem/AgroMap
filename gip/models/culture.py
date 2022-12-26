from django.contrib.gis.db import models

from gip.models.base import BaseModel
from simple_history.models import HistoricalRecords


class Culture(BaseModel):
    name = models.CharField(max_length=55, verbose_name="Культура")
    coefficient_crop = models.FloatField(verbose_name="Коеффициент урожайности")
    history = HistoricalRecords()
    fill_color = models.CharField(max_length=55, default='#3388FF')
    stroke_color = models.CharField(max_length=55, default='#3388FF')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Культура'
        verbose_name_plural = "Культуры"
