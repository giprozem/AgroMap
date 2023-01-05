from django.contrib.gis.db import models

from culture_model.models import Index, Decade, Phase
from gip.models.culture import Culture
from gip.models.region import Region


class IndexPlan(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='index_plans', verbose_name='культуа')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='index_plans', verbose_name='область')
    index = models.ForeignKey(Index, on_delete=models.CASCADE, related_name='index_plans', verbose_name='индекс')
    decade = models.ForeignKey(Decade, on_delete=models.CASCADE, related_name='index_plans', verbose_name='декада')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='index_plans', verbose_name='фаза')
    value = models.DecimalField(max_digits=5, decimal_places=3, default=0, verbose_name='значение индекса')

    class Meta:
        verbose_name = 'Плановое значение индекса'
        verbose_name_plural = "плановые значение индексов"

    def __str__(self):
        return f"значение индекса ({self.value})"
