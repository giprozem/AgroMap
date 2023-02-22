from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.contour import Contour
from gip.models.culture import Culture
from gip.models.farmer import Farmer
from simple_history.models import HistoricalRecords


class LandUse(BaseModel):
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE, related_name='land_uses', verbose_name="Field")
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='land_uses', verbose_name="Farmer")
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='land_uses', verbose_name="Culture")
    year = models.IntegerField(verbose_name="Year")
    season = models.IntegerField(blank=True, null=True, verbose_name="Season")
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.contour}'

    class Meta:
        verbose_name = 'Land use'
        verbose_name_plural = "Land use"


class LandUsePhotos(BaseModel):
    land_use = models.ForeignKey(LandUse, on_delete=models.CASCADE, related_name='land_use_photos')
    image = models.FileField(upload_to='land_use_photos')
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Land use photo'
        verbose_name_plural = "Land use photos"
