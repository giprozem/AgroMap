from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.contour import Contour
from gip.models.culture import Culture
from gip.models.farmer import Farmer


class LandUse(BaseModel):
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE, related_name='land_uses')
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='land_uses')
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='land_uses')
    year = models.IntegerField()
    season = models.IntegerField(blank=True, null=True)


class LandUsePhotos(BaseModel):
    land_use = models.ForeignKey(LandUse, on_delete=models.CASCADE, related_name='land_use_photos')
    image = models.FileField(upload_to='land_use_photos')
