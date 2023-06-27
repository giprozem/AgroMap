from django.contrib.gis.db import models

from gip.models import District


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название Департамента')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"


class ContactInformation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='contact_information',
                                   verbose_name='Департамент')
    title = models.CharField(max_length=255, verbose_name='Наименование госсортстанций и госсортучастков')
    fullname = models.CharField(max_length=255, verbose_name='ФИО руководителя')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='contact_information',
                                 verbose_name='Место расположения')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=125, verbose_name='Телефон', blank=True, null=True)
    mail = models.CharField(max_length=125, verbose_name='Электронный адрес', blank=True, null=True)
    point = models.GeometryField(geography='Kyrgyzstan', verbose_name="Адрес на карте", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Контактные данные"
        verbose_name_plural = "Контактные данные"
