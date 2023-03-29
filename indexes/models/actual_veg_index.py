from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _


class ActualVegIndex(models.Model):
    index_image = models.FileField(upload_to='index_image', verbose_name=_("Изображение индекса"), blank=True)
    average_value = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        verbose_name=_('Средний показатель индекса'),
        blank=True
    )
    meaning_of_average_value = models.ForeignKey(
        'indexes.IndexMeaning',
        on_delete=models.SET_NULL,
        verbose_name=_('Средний показатель индекса'),
        null=True
    )
    index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.CASCADE, verbose_name=_('Индекс'))
    contour = models.ForeignKey('gip.Contour', on_delete=models.CASCADE, verbose_name=_('Контуры поля'),
                                related_name='actual_veg_index')
    date = models.DateField(verbose_name=_('Дата анализа'), help_text=_('Введите дату космо снимка из которого будет высчитан индекс'))
    history = HistoricalRecords(verbose_name=_("История"))

    def __str__(self):
        return f'{self.index} {self.contour}'

    class Meta:
        verbose_name = _('Фактический Индекс')
        verbose_name_plural = _("Фактические Индексы")


class IndexMeaning(models.Model):
    index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.CASCADE, verbose_name=_('Индекс'))
    min_index_value = models.DecimalField(max_digits=4, decimal_places=3, validators=[MinValueValidator(-1)],
                                          verbose_name=_('Минимальное значение'))
    max_index_value = models.DecimalField(max_digits=4, decimal_places=3, validators=[MaxValueValidator(1)],
                                          verbose_name=_('Максимальное значение'))
    description = models.TextField(verbose_name=_('Описание'))

    class Meta:
        verbose_name = _('Значение показателя индекса')
        verbose_name_plural = _("Значение показателей индексов")

    def __str__(self):
        return f'{self.index} {self.min_index_value} {self.max_index_value}'


class PredictedContourVegIndex(models.Model):
    index_image = models.FileField(upload_to='index_image', blank=True)
    average_value = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True
    )
    meaning_of_average_value = models.ForeignKey(
        'indexes.IndexMeaning',
        on_delete=models.SET_NULL,
        null=True
    )
    index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.CASCADE)
    contour = models.ForeignKey('ai.Contour_AI', on_delete=models.CASCADE,
                                related_name='contour_ai_veg_index')
    date = models.DateField()
    history = HistoricalRecords()
