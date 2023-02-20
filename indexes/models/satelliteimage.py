from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords
import rasterio


class SatelliteImages(models.Model):
    # TODO have to refactor code rename variables
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
    bbox = models.CharField(max_length=255, verbose_name='Координаты снимков')

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = 'Спутниковый снимок Sentinel -2'
        verbose_name_plural = "Спутниковые снимки Sentinel -2"

    def save(self, *args, **kwargs):
        with rasterio.open(self.B04) as f:
            B04 = f.bounds

        with rasterio.open(self.B8A) as f:
            B8A = f.bounds

        if B8A == B04:
            # TODO have to optimize code
            self.bbox = B04

        super(SatelliteImages, self).save(*args, **kwargs)


class SatelliteImageSource(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Источник спутниковых снимков'
        verbose_name_plural = "Источники Спутниковых снимков"


class SatelliteImageBand(models.Model):
    band_name = models.CharField(max_length=255, verbose_name='Название диапазона спутникового снимка', unique=True)
    band_description = models.TextField(verbose_name='Описание диапазона спутникового снимка')

    class Meta:
        verbose_name = 'Диапазон спутникового снимка'
        verbose_name_plural = "Диапазоны спутникового снимка"

    def __str__(self):
        return self.band_name


class SatelliteImageLayer(models.Model):
    image = models.FileField(upload_to='satellite_image', verbose_name='Снимок')
    source = models.ForeignKey(
        'indexes.SatelliteImageSource',
        on_delete=models.CASCADE,
        verbose_name='Источник спутниковых снимков',
        related_name='image_source'
    )
    band = models.ForeignKey(
        'indexes.SatelliteImageBand',
        on_delete=models.CASCADE,
        verbose_name='Диапазон спутникового снимка',
        related_name='image_band'
    )

    class Meta:
        verbose_name = 'Слой спутникового снимка'
        verbose_name_plural = "Слои спутниковых снимков"


class SciHubAreaInterest(models.Model):
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Область интересов")


class SciHubImageDate(models.Model):
    area_interest = models.ForeignKey(SciHubAreaInterest, on_delete=models.CASCADE, related_name='image_date')
    date = models.DateTimeField(verbose_name='дата снимков')
    B01 = models.FileField(upload_to='satellite_images', verbose_name='Слой B01', help_text='Coastal aerosol',
                           blank=True, null=True)
    B02 = models.FileField(upload_to='satellite_images', verbose_name='Слой B02', help_text='Blue', blank=True,
                           null=True)
    B03 = models.FileField(upload_to='satellite_images', verbose_name='Слой B03', help_text='Green', blank=True,
                           null=True)
    B04 = models.FileField(upload_to='satellite_images', verbose_name='Слой B04', help_text='Red', blank=True,
                           null=True)
    B05 = models.FileField(upload_to='satellite_images', verbose_name='Слой B05', help_text='Vegetation red edge',
                           blank=True, null=True)
    B06 = models.FileField(upload_to='satellite_images', verbose_name='Слой B06', help_text='Vegetation red edge',
                           blank=True, null=True)
    B07 = models.FileField(upload_to='satellite_images', verbose_name='Слой B07', help_text='Vegetation red edge',
                           blank=True, null=True)
    B08 = models.FileField(upload_to='satellite_images', verbose_name='Слой B08', help_text='NIR', blank=True,
                           null=True)
    B8A = models.FileField(upload_to='satellite_images', verbose_name='Слой B8A', help_text='Narrow NIR', blank=True,
                           null=True)
    B09 = models.FileField(upload_to='satellite_images', verbose_name='Слой B09', help_text='Water vapour', blank=True,
                           null=True)
    B10 = models.FileField(upload_to='satellite_images', verbose_name='Слой B10', help_text='SWIR – Cirrus', blank=True,
                           null=True)
    B11 = models.FileField(upload_to='satellite_images', verbose_name='Слой B11', help_text='SWIR – 1', blank=True,
                           null=True)
    B12 = models.FileField(upload_to='satellite_images', verbose_name='Слой B12', help_text='SWIR - 2', blank=True,
                           null=True)
    history = HistoricalRecords(verbose_name="История")
