from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from indexes.models.satelliteimage import SciHubImageDate


class ActualVegIndex(models.Model):
    index_image = models.FileField(upload_to='index_image', verbose_name=_("Index Image"), blank=True)
    average_value = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        verbose_name=_('Average Index Value'),
        blank=True
    )
    meaning_of_average_value = models.ForeignKey(
        'indexes.IndexMeaning',
        on_delete=models.SET_NULL,
        verbose_name=_('Meaning of Average Index Value'),
        null=True
    )
    index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.CASCADE, verbose_name=_('Index'))
    contour = models.ForeignKey('gip.Contour', on_delete=models.CASCADE, verbose_name=_('Field Contours'),
                                related_name='actual_veg_index')
    date = models.DateField(verbose_name=_('Analysis Date'),
                            help_text=_('Enter the date of the satellite image used to calculate the index'))
    history = HistoricalRecords(verbose_name=_("History"))
    satellite_image = models.ForeignKey(SciHubImageDate, on_delete=models.SET_NULL,
                                        null=True)

    def __str__(self):
        return f'{self.index} {self.contour}'

    class Meta:
        verbose_name = _('Actual Index')
        verbose_name_plural = _("Actual Indices")
        unique_together = (
            'average_value',
            'meaning_of_average_value',
            'index',
            'contour',
            'date'
        )


class IndexMeaning(models.Model):
    index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.CASCADE, verbose_name=_('Index'))
    min_index_value = models.DecimalField(max_digits=4, decimal_places=3, validators=[MinValueValidator(-1)],
                                          verbose_name=_('Minimum Value'))
    max_index_value = models.DecimalField(max_digits=4, decimal_places=3, validators=[MaxValueValidator(1)],
                                          verbose_name=_('Maximum Value'))
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Index Value')
        verbose_name_plural = _("Index Values")

    def __str__(self):
        return f'{self.index} {self.min_index_value} {self.max_index_value}'


class PredictedContourVegIndex(models.Model):
    index_image = models.FileField(upload_to='index_image', blank=True, verbose_name=_('Image'))
    average_value = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True,
        verbose_name=_('Average Index Value')
    )
    meaning_of_average_value = models.ForeignKey(
        'indexes.IndexMeaning',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Index Value')
    )
    index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.CASCADE, verbose_name=_('Index'))
    contour = models.ForeignKey('ai.Contour_AI', on_delete=models.CASCADE,
                                related_name='contour_ai_veg_index', verbose_name=_('Contour'))
    date = models.DateField(verbose_name=_('Analysis Date'))
    history = HistoricalRecords(verbose_name=_("History"))

    class Meta:
        verbose_name = _('AI Index Value')
        verbose_name_plural = _("AI Index Values")

    def __str__(self):
        return f'{self.index}'

