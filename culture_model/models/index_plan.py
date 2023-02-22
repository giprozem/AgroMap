from django.contrib.gis.db import models

from culture_model.models import VegetationIndex, Decade, Phase
from gip.models.culture import Culture
from gip.models.region import Region


class IndexPlan(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='index_plans', verbose_name='Culture')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='index_plans', verbose_name='Region')
    index = models.ForeignKey(VegetationIndex, on_delete=models.CASCADE, related_name='index_plans', verbose_name='Index')
    decade = models.ForeignKey(Decade, on_delete=models.CASCADE, related_name='index_plans', verbose_name='Decade')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='index_plans', verbose_name='Phase')
    value = models.DecimalField(max_digits=5, decimal_places=3, default=0, verbose_name='Index value')

    class Meta:
        verbose_name = 'Planned index value'
        verbose_name_plural = "Planned index values"

    def __str__(self):
        return f"Index value ({self.value})"
