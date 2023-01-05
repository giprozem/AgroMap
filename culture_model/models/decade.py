from django.contrib.gis.db import models


class Decade(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
