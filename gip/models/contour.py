from django.contrib.gis.db import models

from gip.models.conton import Conton
from gip.models.farmer import Farmer


class Contour(models.Model):
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='contours')
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='contours')
    polygon = models.MultiPolygonField()
