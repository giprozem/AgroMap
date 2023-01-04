from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords
from gip.models.contour import Contour


DATE_OF_SATELLITE_IMAGES = (
    ('Весна', '04.05.2022 (Весна)'),
    ('Лето', '15.07.2022 (Лето)'),
    ('Осень', '25.09.2022 (Осень)'),

)


class NDVIIndex(models.Model):
    ndvi_image = models.FileField(upload_to='ndvi_png', blank=True, verbose_name='Картинка NDVI')
    history = HistoricalRecords(verbose_name="История")
    contour = models.ForeignKey(Contour, on_delete=models.SET_NULL, null=True, verbose_name='Контуры Поля')
    date_of_satellite_image = models.CharField(choices=DATE_OF_SATELLITE_IMAGES, verbose_name='Дата космоснимка', max_length=5)

    class Meta:
        verbose_name = 'Индекс NDVI'
        verbose_name_plural = "Индексы NDVI"

    def __str__(self):
        return self.contour.ink
