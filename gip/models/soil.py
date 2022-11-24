from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.fertility import Fertility


class SoilClass(BaseModel):
    name = models.CharField(max_length=55)
    fertility = models.ForeignKey(Fertility, on_delete=models.CASCADE, related_name='soil_classes')

    def __str__(self):
        return self.name

class SoilClassMap(BaseModel):
    soil_class = models.ForeignKey(SoilClass, on_delete=models.CASCADE, related_name='soil_class_maps')
    polygon = models.MultiPolygonField()


class SoilProductivity(BaseModel):
    name = models.CharField(max_length=255)


class SoilFertility(BaseModel):
    soil_productivity = models.ForeignKey(SoilProductivity, on_delete=models.CASCADE, related_name='soil_fertility')
    polygon = models.MultiPolygonField()
