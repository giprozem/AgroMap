from django.contrib.gis.db import models
from gip.models.base import BaseModel


class Fertility(BaseModel):
    name = models.CharField(max_length=255)
