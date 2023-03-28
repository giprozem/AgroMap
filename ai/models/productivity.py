from django.contrib.gis.db import models

from gip.models import BaseModel


class ProductivityML(BaseModel):
    ml_model = models.FileField(upload_to='productivity/')
