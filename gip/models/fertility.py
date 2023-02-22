from django.contrib.gis.db import models
from gip.models.base import BaseModel
from simple_history.models import HistoricalRecords


class Fertility(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Fertilizer")
    history = HistoricalRecords(excluded_fields=['name_ru', 'name_en', 'name_ky'])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fertilizer'
        verbose_name_plural = "Fertilizers"
