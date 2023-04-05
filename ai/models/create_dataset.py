from gip.models.base import BaseModel
from django.contrib.gis.db import models


class Dataset(BaseModel):
    zip = models.FileField(upload_to='zip/')
