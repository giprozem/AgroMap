from django.contrib.gis.db import models

from gip.models.base import BaseModel
from django.utils.translation import gettext_lazy as _


class OrthoPhoto(BaseModel):
    layer_name = models.CharField(max_length=55, verbose_name=_('Название слоя'))
    url = models.URLField(max_length=1024, verbose_name=_('Ссылка'))
    use_y_n = models.BooleanField(verbose_name=_('Используется'))
    file = models.FileField(upload_to='ortho_photo', verbose_name=_("Спутниковое изображение"))

    def __str__(self):
        return self.layer_name

    class Meta:
        verbose_name = _("Спутниковое изображение")
        verbose_name_plural = _("Спутниковые изображения")
