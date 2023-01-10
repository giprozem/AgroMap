from django.contrib.gis.db import models

from hub.models import BaseModel


class DocumentTypeList(BaseModel):
    type_name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = 'Правоустанавливающие документы'
        verbose_name_plural = "Правоустанавливающие документы"