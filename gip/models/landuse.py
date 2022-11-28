from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.contour import Contour
from gip.models.culture import Culture
from gip.models.farmer import Farmer


class LandUse(BaseModel):
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE, related_name='land_uses', verbose_name="Поле")
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='land_uses', verbose_name="Фермер")
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='land_uses', verbose_name="Культура")
    year = models.IntegerField(verbose_name="Год")
    season = models.IntegerField(blank=True, null=True, verbose_name="Сезон")

    def __str__(self):
        return f'{self.contour}'

    class Meta:
        verbose_name = 'Землепользование'
        verbose_name_plural = "Земепользования"


class LandUsePhotos(BaseModel):
    land_use = models.ForeignKey(LandUse, on_delete=models.CASCADE, related_name='land_use_photos')
    image = models.FileField(upload_to='land_use_photos')

    class Meta:
        verbose_name = 'Фото землепользования'
        verbose_name_plural = "Фото земепользования"
