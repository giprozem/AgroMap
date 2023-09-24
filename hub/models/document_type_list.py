from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from hub.models import BaseModel


class DocumentTypeList(BaseModel):

    """
    The DocumentTypeList model is designed to store a list of legal document types. 
    It includes a field for the document name (type_name) and 
    inherits timestamp fields (created_at and updated_at) from the BaseModel abstract model.
    """

    type_name = models.CharField(max_length=50, verbose_name=_('Document Name'))

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = _('Legal Documents')
        verbose_name_plural = _("Legal Documents")
