from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.contour import Contour
from gip.models.culture import Culture
from gip.models.farmer import Farmer
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class LandUse(BaseModel):
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE, related_name='land_uses', verbose_name=_("Поле"))
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='land_uses', verbose_name=_("Фермер"))
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='land_uses', verbose_name=_("Культура"))
    year = models.IntegerField(verbose_name=_("Год"))
    season = models.IntegerField(blank=True, null=True, verbose_name=_("Сезон"))
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.contour}'

    class Meta:
        verbose_name = _("Землепользование")
        verbose_name_plural = _("Землепользование")


class LandUsePhotos(BaseModel):
    land_use = models.ForeignKey(LandUse, on_delete=models.CASCADE, related_name='land_use_photos',
                                 verbose_name=_("Землепользование"))
    image = models.FileField(upload_to='land_use_photos', verbose_name=_("Спутниковое изображение"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Спутниковое изображение")
        verbose_name_plural = _("Спутниковые изображения")
