from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class VegetationIndex(models.Model):

    """
    The VegetationIndex model serves the purpose of defining and representing information about various vegetation indices. 
    It is used to categorize and describe different types of vegetation indices that may be used in applications related to agriculture, 
    environmental monitoring, and more.
    """

    name = models.CharField(max_length=125, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Vegetation Index')
        verbose_name_plural = _('Vegetation Indices')

    def __str__(self):
        return self.name
