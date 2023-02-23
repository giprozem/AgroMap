from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords


class ActualVegIndex(models.Model):
    index_image = models.FileField(upload_to='index_image', verbose_name='Картинка индекса', blank=True)
    average_value = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        verbose_name='Средий показатель индекса',
        blank=True
    )
    meaning_of_average_value = models.ForeignKey(
        'indexes.IndexMeaning',
        on_delete=models.SET_NULL,
        verbose_name='Значение среднего показателя',
        null=True
    )
    index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.CASCADE, verbose_name='Индекс')
    contour = models.ForeignKey('gip.ContourYear', on_delete=models.CASCADE, verbose_name='Контуры Поля', related_name='actual_veg_index')
    date = models.DateField(verbose_name='Дата анализа', help_text='Введите дату космо снимка из которого будет высчитан индекс')
    history = HistoricalRecords(verbose_name="История")

    def __str__(self):
        return f'{self.index} {self.contour}'

    class Meta:
        verbose_name = 'Фактический Индекс'
        verbose_name_plural = "Фактические Индексы"


class IndexMeaning(models.Model):
    index = models.ForeignKey('culture_model.VegetationIndex', on_delete=models.CASCADE, verbose_name='Индекс')
    min_index_value = models.DecimalField(max_digits=4, decimal_places=3, validators=[MinValueValidator(-1)], verbose_name='Минимальное значение')
    max_index_value = models.DecimalField(max_digits=4, decimal_places=3, validators=[MaxValueValidator(1)], verbose_name='Максимальное значение')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Значение показателя индекса'
        verbose_name_plural = "Значение показателей индексов"

    def __str__(self):
        return f'{self.index} {self.min_index_value} {self.max_index_value}'
