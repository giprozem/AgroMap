from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    is_staff = models.BooleanField(default=False, verbose_name=_('Администратор'))
    is_farmer = models.BooleanField(default=False, verbose_name=_('Фермер'))
    is_employee = models.BooleanField(default=False, verbose_name=_('Сотрудник'))
    is_supervisor = models.BooleanField(default=False, verbose_name=_('Руководитель'))
    first_name = None
    last_name = None

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.username


class Profile(models.Model):
    my_user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True, related_name='profiles',
                                   verbose_name=_('Пользователь'))
    full_name = models.CharField(max_length=55, verbose_name=_('ФИО'))
    phone_number = models.CharField(max_length=14, verbose_name=_('Номер телефона'))

    class Meta:
        verbose_name = _('Профиль')
        verbose_name_plural = _('Профили')

    def __str__(self):
        return self.my_user.username
