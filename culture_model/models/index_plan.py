from django.contrib.gis.db import models

from culture_model.models import VegetationIndex, Decade, Phase
from gip.models.culture import Culture
from gip.models.region import Region
from django.utils.translation import gettext_lazy as _


class IndexPlan(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='index_plans',
                                verbose_name=_('Culture'))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='index_plans', verbose_name=_('Region'))
    index = models.ForeignKey(VegetationIndex, on_delete=models.CASCADE, related_name='index_plans',
                              verbose_name=_('Index'))
    decade = models.ForeignKey(Decade, on_delete=models.CASCADE, related_name='index_plans', verbose_name=_('Decade'))
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='index_plans', verbose_name=_('Phase'))
    value = models.DecimalField(max_digits=5, decimal_places=3, default=0, verbose_name=_('Index Value'))

    class Meta:
        verbose_name = _('Planned Index Value')
        verbose_name_plural = _('Planned Index Values')

    def __str__(self):
        return f"Index Value ({self.value})"
