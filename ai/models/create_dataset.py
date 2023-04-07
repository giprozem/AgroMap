from gip.models.base import BaseModel
from django.contrib.gis.db import models
from solo.models import SingletonModel


class Dataset(BaseModel):
    zip = models.FileField(upload_to='zip/')


class Process(SingletonModel):
    is_running = models.BooleanField()
    type_of_process = models.IntegerField()


class Merge_Bands(SingletonModel):
    is_passed = models.BooleanField()
    type_of_process = models.IntegerField()


class Create_RGB(SingletonModel):
    is_passed = models.BooleanField()
    type_of_process = models.IntegerField()


class Cut_RGB_TIF(SingletonModel):
    is_passed = models.BooleanField()
    type_of_process = models.IntegerField()


class AI_Found(SingletonModel):
    is_passed = models.BooleanField()
