from django.contrib.auth import get_user_model # User
from django.contrib.gis.db import models


class Plot(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, blank=True, null=True, related_name='plots')
    name = models.CharField(max_length=125, blank=True, null=True)
    region = models.CharField(max_length=125, blank=True, null=True)
    geometry = models.MultiPolygonField()


class Culture(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='cultures')
    what = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)