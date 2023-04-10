from gip.models.base import BaseModel
from django.contrib.gis.db import models
from solo.models import SingletonModel
from django.utils.translation import gettext_lazy as _


class Dataset(BaseModel):
    zip = models.FileField(upload_to='zip/',  verbose_name=_('Датасет'))

    class Meta:
        verbose_name = _("Датасет")
        verbose_name_plural = _("Датасеты")


class Process(SingletonModel):
    is_running = models.BooleanField(verbose_name=_('Выполняется'))
    type_of_process = models.IntegerField(verbose_name=_('Номер процесса'))

    class Meta:
        verbose_name = _("Процесс")
        verbose_name_plural = _("Процесс")


class Merge_Bands(SingletonModel):
    is_passed = models.BooleanField(verbose_name=_('Завершен'))
    type_of_process = models.IntegerField(verbose_name=_('Номер процесса'))

    class Meta:
        verbose_name = _("Процесс сбора изображений")
        verbose_name_plural = _("Процесс сбора изображений")

class Create_RGB(SingletonModel):
    is_passed = models.BooleanField(verbose_name=_('Завершен'))
    type_of_process = models.IntegerField(verbose_name=_('Номер процесса'))

    class Meta:
        verbose_name = _("Процесс создание цветных изображений")
        verbose_name_plural = _("Процесс создание цветных изображений")


class Cut_RGB_TIF(SingletonModel):
    is_passed = models.BooleanField(verbose_name=_('Завершен'))
    type_of_process = models.IntegerField(verbose_name=_('Номер процесса'))

    class Meta:
        verbose_name = _("Процесс обрезания цветных изображений")
        verbose_name_plural = _("Процесс обрезания цветных изображений")

class AI_Found(SingletonModel):
    is_passed = models.BooleanField(verbose_name=_('Завершен'))

    class Meta:
        verbose_name = _("Процесс поиска контуров")
        verbose_name_plural = _("Процесс поиска контуров")
