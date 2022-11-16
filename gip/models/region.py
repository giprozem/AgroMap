from django.contrib.gis.db import models


class Region(models.Model):
    name = models.CharField(max_length=55)
    population = models.IntegerField()
    area = models.IntegerField()
    density = models.FloatField()