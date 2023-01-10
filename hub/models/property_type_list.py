from django.contrib.gis.db import models

from hub.models import BaseModel


class PropertyTypeList(BaseModel):
    type_name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = 'Данные о собственности'
        verbose_name_plural = "Данные о собственности"