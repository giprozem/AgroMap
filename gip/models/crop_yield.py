from django.contrib.gis.db import models

from gip.models import Contour
from gip.models.base import BaseModel
from gip.models.culture import Culture
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class CropYield(BaseModel):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='crop_yields',
                                verbose_name=_("Culture"))
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE, related_name='crop_yields', verbose_name=_("Field"))
    weight = models.FloatField(help_text=_("Measured in centners"), verbose_name=_("Productivity"))
    year = models.IntegerField(verbose_name=_("Year"))
    season = models.IntegerField(blank=True, null=True, verbose_name=_("Season"))
    history = HistoricalRecords()

    def __str__(self):
        return self.culture.name

    class Meta:
        verbose_name = _("Crop Yield")
        verbose_name_plural = _("Crop Yields")

