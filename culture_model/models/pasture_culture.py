from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from gip.models import District
from gip.models.base import BaseModel
from culture_model.models.phase import Phase


class Classes(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description'
        )
        verbose_name = _('Класс')
        verbose_name_plural = _('Классы')


class Subclass(BaseModel):
    classes = models.ForeignKey(Classes, on_delete=models.SET_NULL, null=True, related_name='subclasses',
                                verbose_name=_('Класс'))
    name = models.CharField(max_length=20, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description',
            'classes',
        )
        verbose_name = _('Подкласс')
        verbose_name_plural = _('Подклассы')


class GroupType(BaseModel):
    subclass = models.ForeignKey(Subclass, on_delete=models.SET_NULL, null=True, related_name='group_type',
                                 verbose_name=_('Подкласс'))
    name = models.CharField(max_length=20, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description',
            'subclass',
        )
        verbose_name = _('Тип группы')
        verbose_name_plural = _('Типы группы')


class RepublicanType(BaseModel):
    type_group = models.ForeignKey(GroupType, on_delete=models.SET_NULL, null=True, related_name='republican_type',
                                   verbose_name=_('Тип группы'))
    name = models.CharField(max_length=20, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description',
            'type_group',
        )
        verbose_name = _('Тип растительности')
        verbose_name_plural = _('Типы растительностей')


class DistrictType(BaseModel):
    type_group = models.ForeignKey(RepublicanType, on_delete=models.SET_NULL, null=True, related_name='district_type',
                                   verbose_name=_('Тип растительности'))
    name = models.CharField(max_length=20, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, verbose_name=_('Район'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'type_group',
            'name',
            'description',
            'district'
        )
        verbose_name = _('Тип района')
        verbose_name_plural = _('Типы районов')


class PastureCulture(BaseModel):
    district_type = models.ForeignKey(DistrictType, on_delete=models.SET_NULL, related_name='pasture_culture',
                                      null=True, verbose_name=_('Тип района'))
    culture_ID = models.CharField(max_length=20)
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    coefficient_to_productivity = models.DecimalField(max_digits=4, decimal_places=2,
                                                      verbose_name=_('Коэффициент продуктивности'))
    content_of_feed = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('Содержание корма'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    veg_period = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'district_type',
            'name',
            'coefficient_to_productivity',
            'content_of_feed',
            'district'
        )
        verbose_name = _('Культура пастбища')
        verbose_name_plural = _('Культуры пастбищ')
