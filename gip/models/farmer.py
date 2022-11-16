from django.contrib.auth import get_user_model
from django.contrib.gis.db import models

from gip.models.base import BaseModel


class Farmer(BaseModel):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='farmers')
    pin_inn = models.CharField(max_length=14)
    mobile = models.CharField(max_length=20)
