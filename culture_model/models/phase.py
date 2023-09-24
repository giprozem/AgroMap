from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Phase(models.Model):

    """
    The Phase model serves the purpose of defining and representing information about development phases. 
    It is used to categorize and describe different phases of development within a system or process.
    """

    name = models.CharField(max_length=125, verbose_name=_('Development Phase'))

    class Meta:
        verbose_name = _('Development Phase')
        verbose_name_plural = _('Development Phases')

    def __str__(self):
        return self.name
