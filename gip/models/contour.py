from django.contrib.gis.db import models

from culture_model.models.pasture_culture import PastureCulture
from gip.models.soil import SoilClass
from gip.models.base import BaseModel
from gip.models.conton import Conton
from gip.models.farmer import Farmer
from gip.models.culture import Culture
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
    code_soato = models.CharField(max_length=30, null=True, blank=True, verbose_name=_("Код СОАТО"))
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='contours', verbose_name=_("Округ"))
    type = models.ForeignKey(LandType, on_delete=models.SET_NULL, null=True, verbose_name=_("Тип земли"),
                             related_name='contours')
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Контур"), blank=True, null=True)
    year = models.CharField(max_length=20, verbose_name=_("Год"), null=True, blank=True)
    productivity = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Продуктивность"))
    predicted_productivity = models.CharField(max_length=20, blank=True, null=True,
                                              verbose_name=_('Прогнозируемая продуктивность'))
    area_ha = models.FloatField(blank=True, null=True, verbose_name=_("Площадь в гектарах"))
    is_deleted = models.BooleanField(default=False, verbose_name=_('Удаленный'))
    culture = models.ForeignKey(Culture, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Культура'))
    pasture_culture = models.ManyToManyField(
        PastureCulture,
        blank=True,
        default=None,
        help_text='Required if land type is pasture',
        verbose_name=_('Культура пастбища')
    )
    elevation = models.CharField(max_length=25, blank=True, null=True, verbose_name=_('Высота'))
    ink = models.CharField(max_length=100, verbose_name=_("ИНК"), help_text=_('Идентификационный номер контура'),
                           null=True, blank=True)
    eni = models.CharField(max_length=100, verbose_name=_("ЕНИ"), null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='contours', verbose_name=_('Фермер'),
                               blank=True, null=True)
    history = HistoricalRecords(verbose_name=_("История"))
    is_rounded = models.BooleanField(default=False, verbose_name=_('Юридически подтвержденный'))
    soil_class = models.ForeignKey(SoilClass, on_delete=models.SET_NULL, blank=True, null=True,
                                   verbose_name='Тип почвы')

    def __str__(self):
        return self.code_soato or self.ink if self.code_soato or self.ink else ''

    class Meta:
        verbose_name = _("Контуры поля")
        verbose_name_plural = _("Контуры полей")


class Elevation(models.Model):
    elevation = models.CharField(max_length=25, blank=True, null=True, verbose_name=_('Высота'))
    point = models.PointField(verbose_name=_("Контур"), blank=True, null=True)

    class Meta:
        verbose_name = _("Высота")
        verbose_name_plural = _("Высоты")
