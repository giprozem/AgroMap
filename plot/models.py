from django.contrib.auth import get_user_model # User
from django.contrib.gis.db import models


class Plot(models.Model):
    user = models.ForeignKey(to=get_user_model(), null=True, blank=False, on_delete=models.SET_NULL, related_name='plots')
    name = models.CharField(max_length=125, blank=True, null=True)
    region = models.CharField(max_length=125, blank=True, null=True)


class Field(models.Model):
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Crop(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, null=True, related_name='crops')
    what = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=55)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('-start',)


class SoilAnalysis(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='soil_analysis')
    photo = models.FileField(upload_to='soil_analysis')
    date = models.DateField()
    description = models.TextField(blank=True, null=True)


class Fertilizer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    field = models.ManyToManyField(Field)
    day_of_fertilizer = models.DateField()


class FieldPolygon(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='polygon_field')
    polygon = models.GeometryField()
    is_actual = models.BooleanField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
