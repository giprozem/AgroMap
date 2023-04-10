from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from hub.models import BaseModel


class PropertyTypeList(BaseModel):
    type_name = models.CharField(max_length=50, verbose_name=_('Название'))

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = _('Данные о собственности')
        verbose_name_plural = _("Данные о собственности")
