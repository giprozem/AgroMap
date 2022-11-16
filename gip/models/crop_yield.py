from django.contrib.gis.db import models

from gip.models.culture import Culture
from gip.models.contour import Contour


class CropYield(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='crop_yields')
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE, related_name='crop_yields')
    weight = models.FloatField(help_text='Indicated in centners')
    year = models.IntegerField()
    season = models.IntegerField(blank=True, null=True)