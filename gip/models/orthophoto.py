from django.contrib.gis.db import models

from gip.models.base import BaseModel
from simple_history.models import HistoricalRecords


class OrthoPhoto(BaseModel):
    layer_name = models.CharField(max_length=55, verbose_name="Layer name")
    url = models.URLField(max_length=1024, verbose_name="Link")
    use_y_n = models.BooleanField(verbose_name="Use")
    file = models.FileField(upload_to='ortho_photo', verbose_name="Satellite image")
    # history = HistoricalRecords()

    def __str__(self):
        return self.layer_name

    class Meta:
        verbose_name = 'Satellite image'
        verbose_name_plural = "Satellite images"
