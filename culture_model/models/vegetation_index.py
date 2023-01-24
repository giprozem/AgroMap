from django.contrib.gis.db import models


class VegetationIndex(models.Model):
    name = models.CharField(max_length=125, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Индекс'
        verbose_name_plural = "Индексы"

    def __str__(self):
        return self.name
