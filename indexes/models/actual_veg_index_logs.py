from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class IndexCreatingReport(models.Model):
    contour = models.ForeignKey('gip.Contour', on_delete=models.SET_NULL, null=True, verbose_name=_('Contour'))
    veg_index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.SET_NULL, null=True,
                                  verbose_name=_('Vegetation Index'))
    satellite_image = models.ForeignKey('indexes.SciHubImageDate', on_delete=models.SET_NULL, null=True,
                                        verbose_name=_('Satellite Image'))
    is_processed = models.BooleanField(default=False, verbose_name=_('Being Processed'))
    process_error = models.TextField(verbose_name=_('Processing Errors'))

    class Meta:
        verbose_name = _("Index Report")
        verbose_name_plural = _("Index Reports")


class ContourAIIndexCreatingReport(models.Model):
    contour = models.ForeignKey('ai.Contour_AI', on_delete=models.SET_NULL, null=True, verbose_name=_("Contour"))
    veg_index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.SET_NULL, null=True,
                                  verbose_name=_("Vegetation Index"))
    satellite_image = models.ForeignKey('indexes.SciHubImageDate', on_delete=models.SET_NULL, null=True,
                                        verbose_name=_("Satellite Image"))
    is_processed = models.BooleanField(default=False, verbose_name=_('Process Initiated'))
    process_error = models.TextField(verbose_name=_('Processing Errors'))

    class Meta:
        verbose_name = _("Index Creation Report")
        verbose_name_plural = _("Index Creation Reports")
