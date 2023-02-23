from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import Area
from django.db.models.signals import post_save
from django.dispatch import receiver

from gip.models.base import BaseModel
from gip.models.conton import Conton
from gip.models.farmer import Farmer
from simple_history.models import HistoricalRecords


class LandType(models.Model):
    name = models.CharField(max_length=125, verbose_name='Name')

    class Meta:
        verbose_name = 'Land type'
        verbose_name_plural = "Land types"

    def __str__(self):
        return self.name


class Contour(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='SOATO code')
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='contours', verbose_name="Canton")
    ink = models.CharField(unique=True, max_length=100, verbose_name='ИНК', help_text='Loop identification number',
                           null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='contours', verbose_name="Farmer",
                               blank=True, null=True)
    history = HistoricalRecords(verbose_name="History")
    is_rounded = models.BooleanField(default=False)

    def __str__(self):
        return self.ink if self.ink else '-'

    class Meta:
        verbose_name = "Field's contours"
        verbose_name_plural = "Fields' contours"


class ContourYear(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='SOATO code')
    contour = models.ManyToManyField(Contour, verbose_name="Fields' contours", related_name='contour_year')
    type = models.ForeignKey(LandType, on_delete=models.SET_NULL, null=True, related_name='contour_year')
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name="Polygon")
    year = models.CharField(max_length=20)
    productivity = models.CharField(max_length=20, blank=True, null=True)
    area_ha = models.FloatField(blank=True, null=True, verbose_name="Area per hectare")


    def __str__(self):
        return self.year or self.code_soato

    class Meta:
        verbose_name = "Field's contours by years"
        verbose_name_plural = "Fields' contours by years"



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
