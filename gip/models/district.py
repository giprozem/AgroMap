from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.region import Region


class District(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=55)
    polygon = models.MultiPolygonField()

    def __str__(self):
        return self.name