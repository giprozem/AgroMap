from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from gip.models import District


class Department(models.Model):

    """
    The Department model is designed to store information about departments or organizational units within an organization. 
    It includes fields for a unique code (unique_code) and the name of the department (name).
    """

    unique_code = models.IntegerField(verbose_name='Unique Code', unique=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_('Department Name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")


class ContactInformation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='contact_information',
                                   verbose_name=_('Department'))
    title = models.CharField(max_length=255, verbose_name=_('Name of State Seed Stations and State Seed Plots'))
    fullname = models.CharField(max_length=255, verbose_name=_('Full Name of Manager'))
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='contact_information',
                                 verbose_name=_('Location'))
    address = models.CharField(max_length=255, verbose_name=_('Address'))
    phone = models.CharField(max_length=125, verbose_name=_('Phone'), blank=True, null=True)
    mail = models.CharField(max_length=125, verbose_name=_('Email'), blank=True, null=True)
    point = models.GeometryField(geography='Kyrgyzstan', verbose_name=_("Map Address"), blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Contact Information")
        verbose_name_plural = _("Contact Information")
