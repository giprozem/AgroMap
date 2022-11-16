from django.contrib.gis.db import models

from gip.models.fertility import Fertility


class SoilClass(models.Model):
    name = models.CharField(max_length=55)
    fertility = models.ForeignKey(Fertility, on_delete=models.CASCADE, related_name='soil_classes')


class SoilClassMap(models.Model):
    soil_class = models.ForeignKey(SoilClass, on_delete=models.CASCADE, related_name='soil_class_maps')
    polygon = models.MultiPolygonField()


class SoilProductivity(models.Model):
    name = models.CharField(max_length=255)


class SoilFertility(models.Model):
    soil_productivity = models.ForeignKey(SoilProductivity, on_delete=models.CASCADE, related_name='soil_fertility')
    polygon = models.MultiPolygonField()
