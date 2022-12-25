from django.contrib.gis.db import models


class NDVIIndex(models.Model):
    coordinates = models.FileField(upload_to='coordinates_geojson', verbose_name='Координаты')
    ndvi_image = models.FileField(upload_to='ndvi_png', blank=True, verbose_name='Картинка NDVI')

    class Meta:
        verbose_name = 'Индекс NDVI'
        verbose_name_plural = "Индексы NDVI"
