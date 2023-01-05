from django.contrib.gis.db import models

from culture_model.models import Index, Decade, Phase
from gip.models.culture import Culture
from gip.models.region import Region


class IndexPlan(models.Model):
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE, related_name='index_plans')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='index_plans')
    index = models.ForeignKey(Index, on_delete=models.CASCADE, related_name='index_plans')
    decade = models.ForeignKey(Decade, on_delete=models.CASCADE, related_name='index_plans')
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name='index_plans')
    value = models.DecimalField(max_digits=5, decimal_places=3, default=0)
