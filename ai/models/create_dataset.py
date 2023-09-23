from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from gip.models.base import BaseModel


class Dataset(BaseModel):
    zip = models.FileField(upload_to='zip/', verbose_name=_('Dataset'))

    class Meta:
        verbose_name = _("Dataset")
        verbose_name_plural = _("Datasets")


class Process(SingletonModel):
    is_running = models.BooleanField(verbose_name=_('Performed'))
    type_of_process = models.IntegerField(verbose_name=_('Process number'))

    class Meta:
        verbose_name = _("Process")
        verbose_name_plural = _("Processes")


class Merge_Bands(SingletonModel):
    is_passed = models.BooleanField(verbose_name=_('Completed'))
    type_of_process = models.IntegerField(verbose_name=_('Process number'))

    class Meta:
        verbose_name = _("Image collection process")
        verbose_name_plural = _("Image collection process")


class Create_RGB(SingletonModel):
    is_passed = models.BooleanField(verbose_name=_('Completed'))
    type_of_process = models.IntegerField(verbose_name=_('Process number'))

    class Meta:
        verbose_name = _("The process of creating color images")
        verbose_name_plural = _("The process of creating color images")


class Cut_RGB_TIF(SingletonModel):
    is_passed = models.BooleanField(verbose_name=_('Completed'))
    type_of_process = models.IntegerField(verbose_name=_('Process number'))

    class Meta:
        verbose_name = _("Process of cropping color images")
        verbose_name_plural = _("Process of cropping color images")


class AI_Found(SingletonModel):
    is_passed = models.BooleanField(verbose_name=_('Completed'))

    class Meta:
        verbose_name = _("Contour search process")
        verbose_name_plural = _("Contour search process")


class CreateDescription(SingletonModel):
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _("Instructions for creating a dataset")
        verbose_name_plural = _("Instructions for creating a dataset")
