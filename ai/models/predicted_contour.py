from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from gip.models.contour import LandType
from gip.models.culture import Culture
from gip.models.soil import SoilClass
from gip.models.conton import Conton
from gip.models.district import District


class Images_AI(models.Model):
    image = models.ImageField(upload_to='images_ai', blank=True, verbose_name=_('Изображение'))

    class Meta:
        verbose_name = _("Изображение")
        verbose_name_plural = _("Изображения")


class Contour_AI(models.Model):
    conton = models.ForeignKey(Conton, on_delete=models.SET_NULL, related_name='contour_ai', null=True, blank=True,
                               verbose_name=_("Округ"))
    type = models.ForeignKey(
        LandType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Тип земли"),
        related_name='contour_ai',
        blank=True
    )
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Контур"), blank=True, null=True)
    year = models.CharField(max_length=20, verbose_name=_("Год"), null=True, blank=True)
    productivity = models.CharField(max_length=20, blank=True, verbose_name=_("Продуктивность"))
    area_ha = models.FloatField(blank=True, null=True, verbose_name=_("Площадь в гектарах"))
    is_deleted = models.BooleanField(default=False, verbose_name=_('Удаленный'))
    culture = models.ForeignKey(Culture, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("Культура"))
    elevation = models.CharField(max_length=25, blank=True, null=True, verbose_name=_('Высота'))
    soil_class = models.ForeignKey(SoilClass, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name=_('Тип почвы'))
    percent = models.FloatField(null=True, blank=True, verbose_name=_("Процент"))
    image = models.ForeignKey(Images_AI, on_delete=models.SET_NULL, related_name='contour_ai', blank=True, null=True,
                              verbose_name=_("Изображение"))

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        related_name='contour_ai',
        null=True,
        blank=True,
        verbose_name=_('Район')
    )

    class Meta:
        verbose_name = _("Контур найденный ИИ")
        verbose_name_plural = _("Контуры найденные ИИ")


class Yolo(SingletonModel):
    ai = models.FileField(upload_to='models_ai/', verbose_name=_('Модель'))

    class Meta:
        verbose_name = _("Модель для поиска контуров")
        verbose_name_plural = _("Модели для поиска контуров")
