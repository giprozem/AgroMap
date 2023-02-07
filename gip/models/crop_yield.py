from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.contour import ContourYear
from gip.models.culture import Culture
from simple_history.models import HistoricalRecords


class CropYield(BaseModel):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='crop_yields', verbose_name="Культура")
    contour_year = models.ForeignKey(ContourYear, on_delete=models.CASCADE, related_name='crop_yields', verbose_name="Поле")
    weight = models.FloatField(help_text='Указыается в центнерах', verbose_name="урожайность")
    year = models.IntegerField(verbose_name="год")
    season = models.IntegerField(blank=True, null=True, verbose_name="сезон")
    history = HistoricalRecords()

    def __str__(self):
        return self.culture.name

    class Meta:
        verbose_name = 'Урожайность'
        verbose_name_plural = "Урожайность"
