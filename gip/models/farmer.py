from django.contrib.auth import get_user_model
from django.contrib.gis.db import models

from gip.models.base import BaseModel


class Farmer(BaseModel):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, related_name='farmers', verbose_name="Фермер")
    pin_inn = models.CharField(max_length=14, verbose_name="ПИН или ИНН")
    mobile = models.CharField(max_length=20, verbose_name="номер телефона")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Фермер'
        verbose_name_plural = "Фермеры"
