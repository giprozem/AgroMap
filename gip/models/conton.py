from django.contrib.gis.db import models

from gip.models.district import District


class Conton(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='contons')
    name = models.CharField(max_length=55)
    polygon = models.MultiPolygonField()