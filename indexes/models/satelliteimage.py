import rasterio
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from rasterio import warp
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class SatelliteImageSource(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Источник спутниковых снимков')
        verbose_name_plural = _("Источники спутниковых снимков")


class SatelliteImageBand(models.Model):
    band_name = models.CharField(max_length=255, verbose_name=_('Название диапазона спутникового снимка'), unique=True)
    band_description = models.TextField(verbose_name=_('Описание диапазона спутникового снимка'))

    class Meta:
        verbose_name = _('Диапазон спутникового снимка')
        verbose_name_plural = _("Диапазоны спутникового снимка")

    def __str__(self):
        return self.band_name


class SatelliteImageLayer(models.Model):
    image = models.FileField(upload_to='satellite_image', verbose_name=_('Снимок'))
    source = models.ForeignKey(
        'indexes.SatelliteImageSource',
        on_delete=models.CASCADE,
        verbose_name=_('Источник спутниковых снимков'),
        related_name='image_source'
    )
    band = models.ForeignKey(
        'indexes.SatelliteImageBand',
        on_delete=models.CASCADE,
        verbose_name=_('Диапазон спутникового снимка'),
        related_name='image_band'
    )

    class Meta:
        verbose_name = _('Слой спутникового снимка')
        verbose_name_plural = _("Слои спутниковых снимков")


class SciHubAreaInterest(models.Model):
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Область интереса"))

    class Meta:
        verbose_name = _('Область интереса спутникового снимка')
        verbose_name_plural = _("Области интереса спутникового снимка")


class SciHubImageDate(models.Model):
    name_product = models.CharField(max_length=255, blank=True, null=True)
    area_interest = models.ForeignKey(SciHubAreaInterest, on_delete=models.SET_NULL, related_name='image_date',
                                      verbose_name=_("Область интереса"), blank=True, null=True)
    no_image = models.BooleanField(default=False, blank=True, null=True)  # todo: Translate
    note = models.CharField(max_length=1000, blank=True, null=True)  # todo: Translate
    date = models.DateTimeField(verbose_name=_('Дата снимков'), blank=True, null=True)
    B01 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B01'), help_text='Coastal aerosol',
                           blank=True, null=True)
    B02 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B02'), help_text='Blue', blank=True,
                           null=True)
    B03 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B03'), help_text='Green', blank=True,
                           null=True)
    B04 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B04'), help_text='Red', blank=True,
                           null=True)
    B05 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B05'), help_text='Vegetation red edge',
                           blank=True, null=True)
    B06 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B06'), help_text='Vegetation red edge',
                           blank=True, null=True)
    B07 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B07'), help_text='Vegetation red edge',
                           blank=True, null=True)
    B08 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B08'), help_text='NIR', blank=True,
                           null=True)
    B8A = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B8A'), help_text='Narrow NIR', blank=True,
                           null=True)
    B09 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B09'), help_text='Water vapour',
                           blank=True,
                           null=True)
    B10 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B10'), help_text='SWIR – Cirrus',
                           blank=True,
                           null=True)
    B11 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B11'), help_text='SWIR – 1', blank=True,
                           null=True)
    B12 = models.FileField(upload_to='satellite_images', verbose_name=_('Слой B12'), help_text='SWIR - 2', blank=True,
                           null=True)
    TCI = models.FileField(upload_to='satellite_images', verbose_name='Слой TCI', help_text='RGB', blank=True,
                           null=True)  # todo: Translate
    image_png = models.FileField(upload_to='satellite_images_to_png', blank=True, null=True)  # todo: Translate
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Координаты снимка"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    history = HistoricalRecords(verbose_name=_("История"))

    class Meta:
        verbose_name = _('Спутниковый снимок Sentinel -2')
        verbose_name_plural = _("Спутниковые снимки Sentinel -2")

    # def save(self, *args, **kwargs):
    #     with rasterio.open(self.B04) as src:
    #         bbox_m = src.bounds
    #         bbox = warp.transform_bounds(src.crs, {'init': 'EPSG:4326'}, *bbox_m)
    #         bboxs = Polygon.from_bbox(bbox)
    #     self.polygon = bboxs
    #     super(SciHubImageDate, self).save(*args, **kwargs)
