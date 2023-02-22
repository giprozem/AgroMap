from django.contrib.gis.db import models


class VegetationIndex(models.Model):
    name = models.CharField(max_length=125, verbose_name='Name')
    description = models.TextField(verbose_name='Description')

    class Meta:
        verbose_name = 'Index'
        verbose_name_plural = "Indexes"

    def __str__(self):
        return self.name
