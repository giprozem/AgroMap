from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel

from gip.models.base import BaseModel


class Dataset(BaseModel):

    """
    The Dataset model is designed to store and manage information related to datasets. 
    It includes a file field to upload and store dataset files.
    """
    
    zip = models.FileField(upload_to='zip/', verbose_name=_('Dataset'))

    class Meta:
        verbose_name = _("Dataset")
        verbose_name_plural = _("Datasets")


class Process(SingletonModel):

    """
    The Process model is designed to represent a single process or task within a Django application. 
    It is implemented as a Singleton model, which means that there can only be one instance of this model in the database.
    """
    
    is_running = models.BooleanField(verbose_name=_('Performed'))
    type_of_process = models.IntegerField(verbose_name=_('Process number'))

    class Meta:
        verbose_name = _("Process")
        verbose_name_plural = _("Processes")


class Merge_Bands(SingletonModel):

    """
    The Merge_Bands model is designed to represent a process or task related to merging image bands. 
    It, too, is implemented as a Singleton model, allowing only one instance of this model in the database.
    """
    
    is_passed = models.BooleanField(verbose_name=_('Completed'))
    type_of_process = models.IntegerField(verbose_name=_('Process number'))

    class Meta:
        verbose_name = _("Image collection process")
        verbose_name_plural = _("Image collection process")


class Create_RGB(SingletonModel):

    """
    The Create_RGB model is designed to represent a process or task related to the creation of color images. 
    Like the previous models, it is implemented as a Singleton model, allowing only one instance of this model in the database.
    """

    is_passed = models.BooleanField(verbose_name=_('Completed'))
    type_of_process = models.IntegerField(verbose_name=_('Process number'))

    class Meta:
        verbose_name = _("The process of creating color images")
        verbose_name_plural = _("The process of creating color images")


class Cut_RGB_TIF(SingletonModel):

    """
    The Cut_RGB_TIF model is designed to represent a process or task related to the cropping of color images in TIFF format. 
    Like the previous models, it is implemented as a Singleton model, allowing only one instance of this model in the database.
    """

    is_passed = models.BooleanField(verbose_name=_('Completed'))
    type_of_process = models.IntegerField(verbose_name=_('Process number'))

    class Meta:
        verbose_name = _("Process of cropping color images")
        verbose_name_plural = _("Process of cropping color images")


class AI_Found(SingletonModel):

    """
    The AI_Found model is designed to represent a process or task related to contour search, possibly using artificial intelligence (AI) techniques. 
    Like the previous models, it is implemented as a Singleton model, allowing only one instance of this model in the database.
    """

    is_passed = models.BooleanField(verbose_name=_('Completed'))

    class Meta:
        verbose_name = _("Contour search process")
        verbose_name_plural = _("Contour search process")


class CreateDescription(SingletonModel):

    """
    The CreateDescription model is designed to store instructions or descriptions related to the process of creating a dataset. 
    Like the previous models, it is implemented as a Singleton model, allowing only one instance of this model in the database.
    """

    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _("Instructions for creating a dataset")
        verbose_name_plural = _("Instructions for creating a dataset")
