from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class SatelliteImageSource(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Satellite Image Source')
        verbose_name_plural = _("Satellite Image Sources")


class SatelliteImageBand(models.Model):
    band_name = models.CharField(max_length=255, verbose_name=_('Satellite Image Band Name'), unique=True)
    band_description = models.TextField(verbose_name=_('Satellite Image Band Description'))

    class Meta:
        verbose_name = _('Satellite Image Band')
        verbose_name_plural = _("Satellite Image Bands")

    def __str__(self):
        return self.band_name


class SatelliteImageLayer(models.Model):
    image = models.FileField(upload_to='satellite_image', verbose_name=_('Image'))
    source = models.ForeignKey(
        'indexes.SatelliteImageSource',
        on_delete=models.CASCADE,
        verbose_name=_('Satellite Image Source'),
        related_name='image_source'
    )
    band = models.ForeignKey(
        'indexes.SatelliteImageBand',
        on_delete=models.CASCADE,
        verbose_name=_('Satellite Image Band'),
        related_name='image_band'
    )

    class Meta:
        verbose_name = _('Satellite Image Layer')
        verbose_name_plural = _("Satellite Image Layers")


class SciHubAreaInterest(models.Model):
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Area of Satellite Image Interest"))

    class Meta:
        verbose_name = _('Satellite Image Area of Interest')
        verbose_name_plural = _("Satellite Image Areas of Interest")


class SciHubImageDate(models.Model):
    name_product = models.CharField(max_length=255, blank=True, null=True)
    area_interest = models.ForeignKey(SciHubAreaInterest, on_delete=models.SET_NULL, related_name='image_date',
                                      verbose_name=_("Area of Interest"), blank=True, null=True)
    no_image = models.BooleanField(default=False, blank=True, null=True)
    note = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(verbose_name=_('Image Date'), blank=True, null=True)
    B01 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B01'), help_text='Coastal aerosol',
                           blank=True, null=True)
    B02 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B02'), help_text='Blue', blank=True,
                           null=True)
    B03 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B03'), help_text='Green', blank=True,
                           null=True)
    B04 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B04'), help_text='Red', blank=True,
                           null=True)
    B05 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B05'), help_text='Vegetation red edge',
                           blank=True, null=True)
    B06 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B06'), help_text='Vegetation red edge',
                           blank=True, null=True)
    B07 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B07'), help_text='Vegetation red edge',
                           blank=True, null=True)
    B08 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B08'), help_text='NIR', blank=True,
                           null=True)
    B8A = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B8A'), help_text='Narrow NIR', blank=True,
                           null=True)
    B09 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B09'), help_text='Water vapour',
                           blank=True,
                           null=True)
    B10 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B10'), help_text='SWIR – Cirrus',
                           blank=True,
                           null=True)
    B11 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B11'), help_text='SWIR – 1', blank=True,
                           null=True)
    B12 = models.FileField(upload_to='satellite_images', verbose_name=_('Layer B12'), help_text='SWIR - 2', blank=True,
                           null=True)
    TCI = models.FileField(upload_to='satellite_images', verbose_name='Layer TCI', help_text='RGB', blank=True,
                           null=True)
    image_png = models.FileField(upload_to='satellite_images_to_png', blank=True, null=True)
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Image Coordinates"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    history = HistoricalRecords(verbose_name=_("History"))

    class Meta:
        verbose_name = _('Sentinel-2 Satellite Image')
        verbose_name_plural = _("Sentinel-2 Satellite Images")