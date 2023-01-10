from django.contrib.gis.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="время обновления")

    class Meta:
        abstract = True
