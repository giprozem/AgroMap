from django.contrib.gis.db import models

from gip.models.conton import Conton


class Village(models.Model):
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='villages')
    name = models.CharField(max_length=55)
    polygon = models.MultiPolygonField()