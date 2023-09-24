from django.contrib.gis.db import models

from gip.models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class SoilClass(BaseModel):

    """
    The SoilClass model is designed to store data related to various types of soils. 
    It includes fields for a unique soil ID, soil type name, description, and color.
    """
    
    id_soil = models.BigIntegerField(verbose_name='Soil ID')
    name = models.CharField(max_length=255, verbose_name=_('Soil Type'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    color = models.CharField(max_length=20, null=True, verbose_name=_('Color'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Soil Type')
        verbose_name_plural = _('Soil Types')


class SoilClassMap(BaseModel):

    """
    The SoilClassMap model is designed to establish a relationship between different soil types 
    (defined in the SoilClass model) and geographical contours. 
    It associates each soil type with a specific geographic area represented by a contour.
    """

    soil_class = models.ForeignKey(SoilClass, on_delete=models.CASCADE, related_name='soil_class_maps',
                                   verbose_name=_('Soil Type'))
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_('Contour'))

    class Meta:
        verbose_name = _('Soil Type Contour')
        verbose_name_plural = _('Soil Type Contours')


class SoilProductivity(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Soil Productivity'))

    class Meta:
        verbose_name = _('Soil Productivity')
        verbose_name_plural = _('Soil Productivities')
