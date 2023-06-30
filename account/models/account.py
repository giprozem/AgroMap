from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# The MyUser model extends the built-in User model.
class MyUser(AbstractUser):
    # is_staff, is_farmer, is_employee, and is_supervisor are Boolean fields that indicate the type of user.
    is_staff = models.BooleanField(default=False, verbose_name=_('Администратор'))
    is_farmer = models.BooleanField(default=False, verbose_name=_('Фермер'))
    is_employee = models.BooleanField(default=False, verbose_name=_('Работник'))
    is_supervisor = models.BooleanField(default=False, verbose_name=_('Наблюдатель'))
    first_name = None  # The first_name and last_name fields are not used in this model.
    last_name = None

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    # Return the username when the object is represented as a string.
    def __str__(self):
        return self.username


# The Profile model is linked to the MyUser model with a one-to-one relationship.
class Profile(models.Model):
    my_user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True, related_name='profiles',
                                   verbose_name=_('Пользователь'))
    full_name = models.CharField(max_length=55, verbose_name=_('ФИО'))
    phone_number = models.CharField(max_length=14, verbose_name=_('Номер телефона'))

    class Meta:
        verbose_name = _('Профиль')
        verbose_name_plural = _('Профили')

    # Return the username of the related user when the object is represented as a string.
    def __str__(self):
        return self.my_user.username


# The Notifications model stores notifications for users.
class Notifications(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='notification',
                             verbose_name=_('Пользователь'))
    date = models.DateTimeField(auto_now=True, verbose_name=_('Дата создания'))
    text = models.CharField(max_length=100, verbose_name=_('Текст уведомления'))
    is_read = models.BooleanField(default=False, verbose_name=_('Прочитано'))

    class Meta:
        verbose_name = _('Уведомление')
        verbose_name_plural = _('Уведомления')

    # Return the notification text when the object is represented as a string.
    def __str__(self):
        return self.text
