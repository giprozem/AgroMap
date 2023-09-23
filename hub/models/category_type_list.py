from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from hub.models import BaseModel


class CategoryTypeList(BaseModel):
    type_name = models.CharField(max_length=50, verbose_name=_('Category Name'))

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = _('Land Categories')
        verbose_name_plural = _("Land Categories")
