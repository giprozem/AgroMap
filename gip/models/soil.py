from django.contrib.gis.db import models

from gip.models.base import BaseModel
from gip.models.fertility import Fertility


class SoilClass(BaseModel):
    name = models.CharField(max_length=55, verbose_name="Вид почвы")
    fertility = models.ForeignKey(Fertility, on_delete=models.CASCADE, related_name='soil_classes', verbose_name="Название удобрение")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид почвы'
        verbose_name_plural = "Виды почв"


class SoilClassMap(BaseModel):
    soil_class = models.ForeignKey(SoilClass, on_delete=models.CASCADE, related_name='soil_class_maps', verbose_name="Вид почвы")
    polygon = models.MultiPolygonField(geography='Kyrgyzstan', verbose_name="Контур")

    class Meta:
        verbose_name = 'Контур вида почвы'
        verbose_name_plural = "Контуры вида почвы"


class SoilProductivity(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Продуктивность почвы")

    class Meta:
        verbose_name = 'Продуктивность почвы'
        verbose_name_plural = "Продуктивность почв"


class SoilFertility(BaseModel):
    soil_productivity = models.ForeignKey(SoilProductivity, on_delete=models.CASCADE, related_name='soil_fertility', verbose_name="Продуктивность почвы")
    polygon = models.MultiPolygonField(geography='Kyrgyzstan', verbose_name="Контур")

    class Meta:
        verbose_name = 'Плодородие почвы'
        verbose_name_plural = "Плодородие почв"
