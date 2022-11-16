from django.contrib.gis.db import models

from gip.models.culture import Culture
from gip.models.contour import Contour
from gip.models.farmer import Farmer


class LandUse(models.Model):
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE, related_name='land_uses')
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='land_uses')
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='land_uses')
    year = models.IntegerField()
    season = models.IntegerField(blank=True, null=True)


class LandUsePhotos(models.Model):
    land_use = models.ForeignKey(LandUse, on_delete=models.CASCADE, related_name='land_use_photos')
    image = models.FileField(upload_to='land_use_photos')
