from django.contrib.gis.db import models
from gip.models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class Fertility(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Удобрение"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Удобрение")
        verbose_name_plural = _("Удобрения")
