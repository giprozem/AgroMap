from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    first_name = None
    last_name = None

    class Meta:
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
