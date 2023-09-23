from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from gip.models import District
from gip.models.base import BaseModel
from culture_model.models.phase import Phase


class Classes(BaseModel):
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description'
        )
        verbose_name = _('Class')
        verbose_name_plural = _('Classes')


class Subclass(BaseModel):
    classes = models.ForeignKey(Classes, on_delete=models.SET_NULL, null=True, related_name='subclasses',
                                verbose_name=_('Class'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description',
            'classes',
        )
        verbose_name = _('Subclass')
        verbose_name_plural = _('Subclasses')


class GroupType(BaseModel):
    subclass = models.ForeignKey(Subclass, on_delete=models.SET_NULL, null=True, related_name='group_type',
                                 verbose_name=_('Subclass'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description',
            'subclass',
        )
        verbose_name = _('Group Type')
        verbose_name_plural = _('Group Types')


class RepublicanType(BaseModel):
    type_group = models.ForeignKey(GroupType, on_delete=models.SET_NULL, null=True, related_name='republican_type',
                                   verbose_name=_('Group Type'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'name',
            'description',
            'type_group',
        )
        verbose_name = _('Vegetation Type')
        verbose_name_plural = _('Vegetation Types')


class DistrictType(BaseModel):
    type_group = models.ForeignKey(RepublicanType, on_delete=models.SET_NULL, null=True, related_name='district_type',
                                   verbose_name=_('Vegetation Type'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, verbose_name=_('District'))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (
            'type_group',
            'name',
            'description',
            'district'
        )
        verbose_name = _('District Type')
        verbose_name_plural = _('District Types')


class PastureCulture(BaseModel):
    district_type = models.ForeignKey(DistrictType, on_delete=models.SET_NULL, related_name='pasture_culture',
                                      null=True, verbose_name=_('District Type'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    coefficient_to_productivity = models.DecimalField(max_digits=4, decimal_places=2,
                                                      verbose_name=_('Productivity Coefficient'))
    content_of_feed = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('Feed Content'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, verbose_name=_('District'))
    veg_period = models.ForeignKey(Phase, on_delete=models.SET_NULL, null=True, verbose_name=_('Vegetation Period'))

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
        verbose_name = _('Pasture Culture')
        verbose_name_plural = _('Pasture Cultures')

