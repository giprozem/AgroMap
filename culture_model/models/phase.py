from django.contrib.gis.db import models


class Phase(models.Model):
    name = models.CharField(max_length=125, verbose_name='Название')

    class Meta:
        verbose_name = 'Фаза развития'
        verbose_name_plural = "Фазы развития"

    def __str__(self):
        return self.name
