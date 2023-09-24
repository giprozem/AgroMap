from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Decade(models.Model):
    
    """
    The Decade model serves the purpose of defining and representing a specific decade or a range of years. 
    It allows you to specify a start date and an end date to delineate the time span of a decade.
    """

    start_date = models.DateField(verbose_name=_('From'))
    end_date = models.DateField(verbose_name=_('To'))

    class Meta:
        verbose_name = _('Decade')
        verbose_name_plural = _('Decades')

    def __str__(self):
        return f"From {self.start_date} to {self.end_date}"
