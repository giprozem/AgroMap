from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Area
from django.db.models.signals import post_save
from django.dispatch import receiver

from gip.models.base import BaseModel
from gip.models.conton import Conton
from gip.models.farmer import Farmer
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class LandType(models.Model):
    name = models.CharField(max_length=125, verbose_name=_("Название"))

    class Meta:
        verbose_name = _("Тип земли")
        verbose_name_plural = _("Типы земли")

    def __str__(self):
        return self.name


class Contour(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_("Код СОАТО"))
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='contours', verbose_name=_("Округ"))
    ink = models.CharField(unique=True, max_length=100, verbose_name=_("ИНК"), help_text=_('Идентификационный номер контура'),
                           null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='contours', verbose_name=_('Фермер'),
                               blank=True, null=True)
    history = HistoricalRecords(verbose_name=_("История"))
    is_rounded = models.BooleanField(default=False)

    def __str__(self):
        return self.code_soato if self.code_soato else self.ink

    class Meta:
        verbose_name = _("Контуры поля")
        verbose_name_plural = _("Контуры полей")


class ContourYear(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_("Код СОАТО"))
    contour = models.ManyToManyField(Contour, verbose_name=_("Контуры полей"), related_name='contour_year')
    type = models.ForeignKey(LandType, on_delete=models.SET_NULL, null=True, verbose_name=_("Тип земли"), related_name='contour_year')
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Контур"))
    year = models.CharField(max_length=20, verbose_name=_("Год"))
    productivity = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Продуктивность"))
    area_ha = models.FloatField(blank=True, null=True, verbose_name=_("Площадь в гектарах"))


    def __str__(self):
        return self.year or self.code_soato

    class Meta:
        verbose_name = _("Контуры поля по годам")
        verbose_name_plural = _("Контуры полей по годам")



@receiver(post_save, sender=ContourYear)
def update(sender, instance, created, **kwargs):
    if created:
        geom = ContourYear.objects.annotate(area_=Area("polygon")).get(id=instance.id)
        ha = round(geom.area_.sq_km * 100, 2)
        instance.area_ha = ha
        instance.save()
    else:
        geom = ContourYear.objects.annotate(area_=Area("polygon")).get(id=instance.id)
        ha = round(geom.area_.sq_km * 100, 2)
        ContourYear.objects.filter(id=instance.id).update(area_ha=ha)
