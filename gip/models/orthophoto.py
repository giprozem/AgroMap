from django.contrib.gis.db import models


class OrthoPhoto(models.Model):
    layer_name = models.CharField(max_length=55)
    url = models.URLField(max_length=1024)
    use_y_n = models.BooleanField()
    file = models.FileField(upload_to='ortho_photo')
