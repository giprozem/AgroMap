from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.conton import Conton
from gip.models.farmer import Farmer


class Contour(BaseModel):
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='contours')
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='contours')
    polygon = models.MultiPolygonField(geography='Kyrgyzstan')

    def __str__(self):
        return self.conton.name