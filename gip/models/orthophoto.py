from django.contrib.gis.db import models

from gip.models.base import BaseModel


class OrthoPhoto(BaseModel):
    layer_name = models.CharField(max_length=55, verbose_name="Название слоя")
    url = models.URLField(max_length=1024, verbose_name="Ссылка")
    use_y_n = models.BooleanField(verbose_name="Использовать")
    file = models.FileField(upload_to='ortho_photo', verbose_name="Спутниковый снимок")

    def __str__(self):
        return self.layer_name

    class Meta:
        verbose_name = 'Спутниковый снимок'
        verbose_name_plural = "Спутниковые снимки"
