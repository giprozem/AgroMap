from django.contrib.gis.db import models

from culture_model.models.pasture_culture import PastureCulture
from gip.models.soil import SoilClass
from gip.models.base import BaseModel
from gip.models.conton import Conton
from gip.models.farmer import Farmer
from gip.models.culture import Culture
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class LandType(models.Model):
    """
    The LandType model is designed to store information about different types or categories of land. 
    It includes a single field for the land type name (name).
    """

    name = models.CharField(max_length=125, verbose_name=_("Land Type Name"))

    class Meta:
        verbose_name = _("Land Type")
        verbose_name_plural = _("Land Types")

    def __str__(self):
        return self.name_en


class Contour(BaseModel):
    """
    The Contour model is designed to store information about field contours or land parcels. 
    It includes various fields for attributes such as SOATO codes, district associations, land types, and more.
    """

    code_soato = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("SOATO Code"))
    conton = models.ForeignKey(Conton, on_delete=models.SET_NULL, related_name='contours', verbose_name=_("Conton"),
                               blank=True, null=True)
    type = models.ForeignKey(LandType, on_delete=models.SET_NULL, null=True, verbose_name=_("Land Type"),
                             related_name='contours')
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Contour"), blank=True, null=True)
    year = models.CharField(max_length=20, verbose_name=_("Year"), null=True, blank=True)
    productivity = models.CharField(max_length=20, blank=True, null=True, default='1.0', verbose_name=_("Productivity"))
    month_of_sowing = models.CharField(max_length=20, verbose_name=_("Month of sowing"), null=True, blank=True)
    vegetation_type = models.CharField(max_length=20, blank=True, null=True, verbose_name="Vegetation Type")
    predicted_productivity = models.CharField(max_length=20, blank=True, null=True, default='1.0',
                                              verbose_name=_('Predicted Productivity'))
    area_ha = models.FloatField(blank=True, null=True, verbose_name=_("Area in Hectares"))
    is_deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))
    culture = models.ForeignKey(Culture, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Culture'),
                                related_name='contour_culture')
    predicted_culture = models.ForeignKey(Culture, on_delete=models.SET_NULL, blank=True, null=True,
                                          verbose_name=_('Predicted Culture'), related_name='contour_predicted_culture')
    pasture_culture = models.ManyToManyField(
        PastureCulture,
        blank=True,
        default=None,
        help_text='Required if land type is pasture',
        verbose_name=_('Pasture Culture')
    )
    elevation = models.CharField(max_length=25, blank=True, null=True, verbose_name=_('Elevation'))
    ink = models.CharField(max_length=100, verbose_name=_("INK"), help_text=_('Identification Number of the Contour'),
                           null=True, blank=True)
    eni = models.CharField(max_length=100, verbose_name=_("ENI"), null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='contours', verbose_name=_('Farmer'),
                               blank=True, null=True)
    history = HistoricalRecords(verbose_name=_("History"))
    is_rounded = models.BooleanField(default=False, verbose_name=_('Legally Confirmed'))
    soil_class = models.ForeignKey(SoilClass, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name='Soil Type')
    cadastre = models.BooleanField(default=False)

    def __str__(self):
        return self.code_soato if self.code_soato else '' or self.ink if self.ink else '' or f"{self.pk}" if self.pk else ''

    class Meta:
        verbose_name = _("Field Contour")
        verbose_name_plural = _("Field Contours")
