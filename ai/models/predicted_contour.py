from django.contrib.gis.db import models
from gip.models.conton import Conton
from gip.models.district import District

class Images(models.Model):
    image = models.ImageField(upload_to='media/', blank=True)


class Contour(models.Model):
    polygon = models.GeometryField(geography='Kyrgyzstan', blank=True, null=True)
    percent = models.FloatField(null=True, default=0.5)
    culture = models.CharField(max_length=50, blank=True)
    image = models.ForeignKey(Images, on_delete=models.PROTECT, related_name='images')
    conton = models.ForeignKey(Conton, on_delete=models.PROTECT, related_name='canton', null=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name='district', default=1)
    productivity = models.CharField(max_length=20, blank=True)


class Yolo(models.Model):
    ai = models.FileField(upload_to='models/')
