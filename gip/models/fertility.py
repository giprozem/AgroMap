from django.contrib.gis.db import models


class Fertility(models.Model):
    name = models.CharField(max_length=255)