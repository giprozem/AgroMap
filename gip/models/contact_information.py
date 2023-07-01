from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from gip.models import District


class Department(models.Model):
    unique_code = models.IntegerField(verbose_name='Уникальный код', unique=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_('Название Департамента'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Департамент")
        verbose_name_plural = _("Департаменты")


class ContactInformation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='contact_information',
                                   verbose_name=_('Департамент'))
    title = models.CharField(max_length=255, verbose_name=_('Наименование госсортстанций и госсортучастков'))
    fullname = models.CharField(max_length=255, verbose_name=_('ФИО руководителя'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='contact_information',
                                 verbose_name=_('Место расположения'))
    address = models.CharField(max_length=255, verbose_name=_('Адрес'))
    phone = models.CharField(max_length=125, verbose_name=_('Телефон'), blank=True, null=True)
    mail = models.CharField(max_length=125, verbose_name=_('Электронный адрес'), blank=True, null=True)
    point = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Адрес на карте"), blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Контактные данные")
        verbose_name_plural = _("Контактные данные")
