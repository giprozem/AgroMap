from django.contrib.gis.db import models

from gip.models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class Culture(BaseModel):
    name = models.CharField(max_length=55, verbose_name=_("Культура"))
    coefficient_crop = models.FloatField(verbose_name=_("Коэффициент продуктивности"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Культура")
        verbose_name_plural = _("Культуры")
