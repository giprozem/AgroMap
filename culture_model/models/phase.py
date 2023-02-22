from django.contrib.gis.db import models


class Phase(models.Model):
    name = models.CharField(max_length=125, verbose_name='Name')

    class Meta:
        verbose_name = 'Development phase'
        verbose_name_plural = "Development phases"

    def __str__(self):
        return self.name
