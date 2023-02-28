from django.contrib.gis.db import models

from culture_model.models import VegetationIndex, Decade, Phase
from gip.models.culture import Culture
from gip.models.region import Region
from django.utils.translation import gettext_lazy as _


class IndexPlan(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='index_plans', verbose_name=_('Культура'))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='index_plans', verbose_name=_('Область'))
    index = models.ForeignKey(VegetationIndex, on_delete=models.CASCADE, related_name='index_plans', verbose_name=_('Индекс'))
    decade = models.ForeignKey(Decade, on_delete=models.CASCADE, related_name='index_plans', verbose_name=_('Декада'))
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='index_plans', verbose_name=_('Фаза'))
    value = models.DecimalField(max_digits=5, decimal_places=3, default=0, verbose_name=_('Значение индекса'))

    class Meta:
        verbose_name = _('Плановое значение индекса')
        verbose_name_plural = _('Плановые значения индекса')

    def __str__(self):
        return f"Index value ({self.value})"
