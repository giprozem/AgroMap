from django.contrib.gis.db import models


class Phase(models.Model):
    name = models.CharField(max_length=125)
