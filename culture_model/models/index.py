from django.contrib.gis.db import models


class Index(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField()
