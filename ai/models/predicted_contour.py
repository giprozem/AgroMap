from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from gip.models.contour import LandType
from gip.models.culture import Culture
from gip.models.soil import SoilClass
from gip.models.conton import Conton
from gip.models.district import District


class Images_AI(models.Model):
    image = models.ImageField(upload_to='images_ai', blank=True, verbose_name=_('Image'))

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class Contour_AI(models.Model):
    conton = models.ForeignKey(Conton, on_delete=models.SET_NULL, related_name='contour_ai', null=True, blank=True,
                               verbose_name=_("Region"))
    type = models.ForeignKey(
        LandType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Land type"),
        related_name='contour_ai',
        blank=True
    )
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Contour"), blank=True, null=True)
    year = models.CharField(max_length=20, verbose_name=_("Year"), null=True, blank=True)
    productivity = models.CharField(max_length=20, blank=True, verbose_name=_("Productivity"))
    area_ha = models.FloatField(blank=True, null=True, verbose_name=_("Area in hectares"))
    is_deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))
    culture = models.ForeignKey(Culture, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Culture"))
    elevation = models.CharField(max_length=25, blank=True, null=True, verbose_name=_('Elevation'))
    soil_class = models.ForeignKey(SoilClass, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name=_('Soil Type'))
    percent = models.FloatField(null=True, blank=True, verbose_name=_("Percentage"))
    image = models.ForeignKey(Images_AI, on_delete=models.SET_NULL, related_name='contour_ai', blank=True, null=True,
                              verbose_name=_("Image"))

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        related_name='contour_ai',
        null=True,
        blank=True,
        verbose_name=_('District')
    )

    class Meta:
        verbose_name = _("AI Detected Contour")
        verbose_name_plural = _("AI Detected Contours")


class Yolo(SingletonModel):
    ai = models.FileField(upload_to='models_ai/', verbose_name=_('Model'))

    class Meta:
        verbose_name = _("Contour Detection Model")
        verbose_name_plural = _("Contour Detection Models")
