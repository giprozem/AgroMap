from django.contrib.gis.db import models


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
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_("Код СОАТО"))
    conton = models.ForeignKey(Conton, on_delete=models.CASCADE, related_name='contours', verbose_name=_("Округ"))
    ink = models.CharField(unique=True, max_length=100, verbose_name=_("ИНК"),
                           help_text=_('Идентификационный номер контура'),
                           null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='contours', verbose_name=_('Фермер'),
                               blank=True, null=True)
    history = HistoricalRecords(verbose_name=_("История"))
    is_rounded = models.BooleanField(default=False, verbose_name=_('Юридически подтвержденный'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('Удаленный'))

    def __str__(self):
        return self.code_soato if self.code_soato else self.ink

    class Meta:
        verbose_name = _("Контуры поля")
        verbose_name_plural = _("Контуры полей")


class ContourYear(BaseModel):
    code_soato = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name=_("Код СОАТО"))
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE, verbose_name=_("Контуры полей"),
                                related_name='contour_year')
    type = models.ForeignKey(LandType, on_delete=models.SET_NULL, null=True, verbose_name=_("Тип земли"),
                             related_name='contour_year')
    polygon = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Контур"))
    year = models.CharField(max_length=20, verbose_name=_("Год"))
    productivity = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Продуктивность"))
    area_ha = models.FloatField(blank=True, null=True, verbose_name=_("Площадь в гектарах"))
    is_deleted = models.BooleanField(default=False, verbose_name=_('Удаленный'))
    culture = models.ForeignKey(Culture, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Культура'))
    elevation = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.year or self.code_soato

    class Meta:
        verbose_name = _("Контуры поля по годам")
        verbose_name_plural = _("Контуры полей по годам")


class Elevation(models.Model):
    elevation = models.CharField(max_length=25, blank=True, null=True)
    point = models.PointField(verbose_name=_("Контур"), blank=True, null=True)
