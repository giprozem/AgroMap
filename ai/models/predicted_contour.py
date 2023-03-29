from django.contrib.gis.db import models
from solo.models import SingletonModel

from gip.models.conton import Conton
from gip.models.district import District


class Images_AI(models.Model):
    image = models.ImageField(upload_to='images_ai', blank=True)


class Contour_AI(models.Model):
    polygon = models.GeometryField(geography='Kyrgyzstan', blank=True, null=True)
    percent = models.FloatField(null=True, blank=True)
    culture = models.CharField(max_length=50, blank=True, null=True)
    image = models.ForeignKey(Images_AI, on_delete=models.SET_NULL, related_name='contour_ai', blank=True, null=True)
    conton = models.ForeignKey(Conton, on_delete=models.SET_NULL, related_name='contour_ai', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, related_name='contour_ai', null=True,
                                 blank=True)
    productivity = models.CharField(max_length=20, blank=True)


class Yolo(SingletonModel):
    ai = models.FileField(upload_to='models_ai/')
