from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Phase(models.Model):
    name = models.CharField(max_length=125, verbose_name=_('Development Phase'))

    class Meta:
        verbose_name = _('Development Phase')
        verbose_name_plural = _('Development Phases')

    def __str__(self):
        return self.name
