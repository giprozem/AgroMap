from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords


class SatelliteImages(models.Model):
    region_name = models.CharField(max_length=100, verbose_name='Название региона')
    description = models.TextField(null=True, blank=True, verbose_name='Описание', help_text='Заполняется при необходимости')
    date = models.DateField(verbose_name='дата снимков')
    decade = models.ForeignKey('culture_model.Decade', on_delete=models.CASCADE, verbose_name='Декада')
    B01 = models.FileField(upload_to='satellite_images', verbose_name='Слой B01', help_text='Coastal aerosol', blank=True, null=True)
    B02 = models.FileField(upload_to='satellite_images', verbose_name='Слой B02', help_text='Blue', blank=True, null=True)
    B03 = models.FileField(upload_to='satellite_images', verbose_name='Слой B03', help_text='Green', blank=True, null=True)
    B04 = models.FileField(upload_to='satellite_images', verbose_name='Слой B04', help_text='Red', blank=True, null=True)
    B05 = models.FileField(upload_to='satellite_images', verbose_name='Слой B05', help_text='Vegetation red edge', blank=True, null=True)
    B06 = models.FileField(upload_to='satellite_images', verbose_name='Слой B06', help_text='Vegetation red edge', blank=True, null=True)
    B07 = models.FileField(upload_to='satellite_images', verbose_name='Слой B07', help_text='Vegetation red edge', blank=True, null=True)
    B08 = models.FileField(upload_to='satellite_images', verbose_name='Слой B08', help_text='NIR', blank=True, null=True)
    B8A = models.FileField(upload_to='satellite_images', verbose_name='Слой B8A', help_text='Narrow NIR', blank=True, null=True)
    B09 = models.FileField(upload_to='satellite_images', verbose_name='Слой B09', help_text='Water vapour', blank=True, null=True)
    B10 = models.FileField(upload_to='satellite_images', verbose_name='Слой B10', help_text='SWIR – Cirrus', blank=True, null=True)
    B11 = models.FileField(upload_to='satellite_images', verbose_name='Слой B11', help_text='SWIR – 1', blank=True, null=True)
    B12 = models.FileField(upload_to='satellite_images', verbose_name='Слой B12', help_text='SWIR - 2', blank=True, null=True)
    history = HistoricalRecords(verbose_name="История")

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = 'Спутниковый снимок'
        verbose_name_plural = "Спутниковые снимки"
