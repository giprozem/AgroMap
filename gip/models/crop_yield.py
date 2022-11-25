from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.contour import Contour
from gip.models.culture import Culture
from simple_history.models import HistoricalRecords


class CropYield(BaseModel):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='crop_yields')
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE, related_name='crop_yields')
    weight = models.FloatField(help_text='Indicated in centners')
    year = models.IntegerField()
    season = models.IntegerField(blank=True, null=True)
    history = HistoricalRecords()

    # def __str__(self):
    #     return self