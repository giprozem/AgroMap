from django.contrib.auth import get_user_model
from django.contrib.gis.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Time of creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update time")

    class Meta:
        abstract = True
