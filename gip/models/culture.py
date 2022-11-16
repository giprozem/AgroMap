from django.contrib.gis.db import models


class Culture(models.Model):
    name = models.CharField(max_length=55)
    coefficient_crop = models.FloatField()
