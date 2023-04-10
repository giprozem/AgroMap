from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from gip.models import BaseModel


class ProductivityML(BaseModel):
    ml_model = models.FileField(upload_to='productivity/', verbose_name=_('Модель'))

    class Meta:
        verbose_name = _("Модель для прогноза продуктивности")
        verbose_name_plural = _("Модели для прогноза продуктивности")
