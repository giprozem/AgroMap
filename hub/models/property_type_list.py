from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from hub.models import BaseModel


class PropertyTypeList(BaseModel):
    """
    The PropertyTypeList model is designed to store a list of property types or categories. 
    It includes a field for the property type name (type_name) and inherits timestamp fields (created_at and updated_at) 
    from the BaseModel abstract model.
    """

    type_name = models.CharField(max_length=50, verbose_name=_('Name'))

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = _('Property Type Data')
        verbose_name_plural = _("Property Type Data")
