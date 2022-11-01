from django.contrib.auth import get_user_model # User
from django.contrib.gis.db import models


class Plot(models.Model):
    user = models.ForeignKey(to=get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='plots')
    name = models.CharField(max_length=125, blank=True, null=True)
    region = models.CharField(max_length=125, blank=True, null=True)


class CultureField(models.Model):
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    what = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    geometry = models.GeometryField(null=True)

    class Meta:
        ordering = ('-start',)


class Crop(models.Model):
    culture = models.ForeignKey(CultureField, on_delete=models.CASCADE, null=True, related_name='crops')
    what = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=55)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('-start',)


class Fertilizer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    culture_field = models.ManyToManyField(CultureField)
    day_of_fertilizer = models.DateField()
