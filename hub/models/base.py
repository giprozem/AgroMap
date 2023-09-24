from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):

    """
    The BaseModel abstract model is designed to provide common fields for tracking the creation and last update timestamps for records in models that inherit from it. 
    It serves as a foundation for other models, allowing them to inherit these timestamp fields without repeating the code.
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update Date"))

    class Meta:
        abstract = True

