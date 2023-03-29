from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class IndexCreatingReport(models.Model):
    contour = models.ForeignKey('gip.Contour', on_delete=models.SET_NULL, null=True, verbose_name=_('Контур'))
    veg_index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.SET_NULL, null=True,
                                  verbose_name=_('Вегетационный индекс'))
    satellite_image = models.ForeignKey('indexes.SciHubImageDate', on_delete=models.SET_NULL, null=True,
                                        verbose_name=_('Спутниковое изображение'))
    is_processed = models.BooleanField(default=False, verbose_name=_('Обрабатывается'))
    process_error = models.TextField(verbose_name=_('Ошибки обработки'))

    class Meta:
        verbose_name = _("Отчет по индексу")
        verbose_name_plural = _("Отчеты по индексу")


class ContourAIIndexCreatingReport(models.Model):
    contour = models.ForeignKey('ai.Contour_AI', on_delete=models.SET_NULL, null=True)
    veg_index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.SET_NULL, null=True)
    satellite_image = models.ForeignKey('indexes.SciHubImageDate', on_delete=models.SET_NULL, null=True)
    is_processed = models.BooleanField(default=False)
    process_error = models.TextField()
