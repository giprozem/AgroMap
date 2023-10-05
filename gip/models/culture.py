from django.contrib.gis.db import models

from gip.models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class Culture(BaseModel):

    """
    The Culture model is designed to store data related to different types of agricultural crops or cultures.
    It includes fields for the name of the culture and a coefficient representing crop productivity.
    """

    name = models.CharField(max_length=55, verbose_name=_("Culture"))
    coefficient_crop = models.FloatField(
        verbose_name=_("Crop Productivity Coefficient"),
        default=0.0
    )
    culture_type = models.ForeignKey(
        "gip.CultureType",
        verbose_name=_("Type"),
        related_name="culture_id",
        on_delete=models.DO_NOTHING,
        null=True,
    )   


    class Meta:
        verbose_name = _("Culture")
        verbose_name_plural = _("Cultures")

    def __str__(self):
        return self.name


class CultureType(BaseModel):
    name = models.CharField(max_length=55, verbose_name=_("Culture type"), null=True, blank=True)


    class Meta:
        verbose_name = _("Culture type")
        verbose_name_plural = _("Cultures types")

    def __str__(self):
        return self.name