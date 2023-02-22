from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.contour import ContourYear
from gip.models.culture import Culture
from simple_history.models import HistoricalRecords


class CropYield(BaseModel):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='crop_yields', verbose_name="Culture")
    contour_year = models.ForeignKey(ContourYear, on_delete=models.CASCADE, related_name='crop_yields', verbose_name="Field")
    weight = models.FloatField(help_text='Indicated in centners', verbose_name="Productivity")
    year = models.IntegerField(verbose_name="Year")
    season = models.IntegerField(blank=True, null=True, verbose_name="Season")
    history = HistoricalRecords()

    def __str__(self):
        return self.culture.name

    class Meta:
        verbose_name = 'Productivity'
        verbose_name_plural = "Productivity"
