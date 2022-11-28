from django.contrib.gis.db import models
from gip.models.base import BaseModel
from simple_history.models import HistoricalRecords


class Fertility(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Наименование удобрения")
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Удобрение'
        verbose_name_plural = "Удобрения"
