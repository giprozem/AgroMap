from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords


class NDVIIndex(models.Model):
    coordinates = models.FileField(upload_to='coordinates_geojson', verbose_name='Координаты')
    ndvi_image = models.FileField(upload_to='ndvi_png', blank=True, verbose_name='Картинка NDVI')
    history = HistoricalRecords(verbose_name="История")

    class Meta:
        verbose_name = 'Индекс NDVI'
        verbose_name_plural = "Индексы NDVI"

    def __str__(self):
        return self.coordinates.name
