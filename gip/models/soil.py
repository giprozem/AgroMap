from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.fertility import Fertility
from simple_history.models import HistoricalRecords


class SoilClass(BaseModel):
    name = models.CharField(max_length=55, verbose_name="Soil type")
    fertility = models.ForeignKey(Fertility, on_delete=models.CASCADE, related_name='soil_classes', verbose_name="Fertilizer")
    # history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Soil type'
        verbose_name_plural = "Soil types"


class SoilClassMap(BaseModel):
    soil_class = models.ForeignKey(SoilClass, on_delete=models.CASCADE, related_name='soil_class_maps', verbose_name="Soil type")
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Polygon")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'The polygon of soil type'
        verbose_name_plural = "Polygons of soil type"


class SoilProductivity(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Soil productivity")
    # history = HistoricalRecords()

    class Meta:
        verbose_name = 'Soil productivity'
        verbose_name_plural = "Soils' productivity"


class SoilFertility(BaseModel):
    soil_productivity = models.ForeignKey(SoilProductivity, on_delete=models.CASCADE, related_name='soil_fertility', verbose_name="Soil productivity")
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Polygon")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Soil fertility'
        verbose_name_plural = "Soils' fertility"
