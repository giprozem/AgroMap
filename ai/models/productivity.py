from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from gip.models import BaseModel


class ProductivityML(BaseModel):
    
    """
    The ProductivityML model is designed to store a machine learning model file used for productivity prediction.
    """

    ml_model = models.FileField(upload_to='productivity/', verbose_name=_('Model'))

    class Meta:
        verbose_name = _("Productivity Prediction Model")
        verbose_name_plural = _("Productivity Prediction Models")
