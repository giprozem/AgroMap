from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.region import Region
from simple_history.models import HistoricalRecords


class District(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='Soato code')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts', verbose_name="Region")
    name = models.CharField(max_length=55, verbose_name="District")
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Polygon")
    history = HistoricalRecords(excluded_fields=['name_ru', 'name_en', 'name_ky'])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'District'
        verbose_name_plural = "Districts"
