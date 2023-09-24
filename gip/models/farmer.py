from django.contrib.gis.db import models

from account.models import MyUser
from gip.models.base import BaseModel
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class Farmer(BaseModel):

    """
    The Farmer model is designed to store data related to individuals who work as farmers. 
    It includes fields for the farmer's user profile, Taxpayer Identification Number (TIN) or Personal Identification Number (INN), 
    and phone number.    
    """
    
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='farmers', verbose_name=_("Farmer"))
    pin_inn = models.CharField(max_length=14, verbose_name=_("TIN or INN"),
                               help_text=_("Taxpayer Identification Number or Personal Identification Number"))
    mobile = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    history = HistoricalRecords()

    def __str__(self):
        return self.pin_inn

    class Meta:
        verbose_name = _("Farmer")
        verbose_name_plural = _("Farmers")
