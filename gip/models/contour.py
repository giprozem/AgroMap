from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Area
from django.db.models.signals import post_save
from django.dispatch import receiver

from gip.models.base import BaseModel
from gip.models.conton import Conton
from gip.models.farmer import Farmer
from simple_history.models import HistoricalRecords


class Contour(BaseModel):
    ink = models.CharField(max_length=100, verbose_name='ИНК', help_text='Идентификационный Номер Контура', null=True, blank=False)
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='contours', verbose_name="Айылный аймак")
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='contours', verbose_name="Фермер")
    polygon = models.MultiPolygonField(geography='Kyrgyzstan', verbose_name="Контур")
    sum_ha = models.FloatField(blank=True, null=True, verbose_name="Площадь га")
    history = HistoricalRecords(verbose_name="История")

    def __str__(self):
        return self.conton.name

    class Meta:
        verbose_name = 'Контуры Поля'
        verbose_name_plural = "Контуры полей"


@receiver(post_save, sender=Contour)
def update(sender, instance, created, **kwargs):
    if created:
        geom = Contour.objects.annotate(area_=Area("polygon")).get(id=instance.id)
        ha = round(geom.area_.sq_km * 100, 2)
        instance.sum_ha = ha
        instance.save()
    else:
        geom = Contour.objects.annotate(area_=Area("polygon")).get(id=instance.id)
        ha = round(geom.area_.sq_km * 100, 2)
        Contour.objects.filter(id=instance.id).update(sum_ha=ha)
