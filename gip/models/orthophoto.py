from django.contrib.gis.db import models

from gip.models.base import BaseModel


class OrthoPhoto(BaseModel):
    layer_name = models.CharField(max_length=55)
    url = models.URLField(max_length=1024)
    use_y_n = models.BooleanField()
    file = models.FileField(upload_to='ortho_photo')
