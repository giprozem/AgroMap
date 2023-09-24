from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from hub.models import BaseModel


class CategoryTypeList(BaseModel):

    """
    The CategoryTypeList model is designed to store a list of land categories or types. 
    It includes a field for the category name (type_name) and 
    inherits timestamp fields (created_at and updated_at) from the BaseModel abstract model.
    """

    type_name = models.CharField(max_length=50, verbose_name=_('Category Name'))

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = _('Land Categories')
        verbose_name_plural = _("Land Categories")
