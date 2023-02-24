from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords

from indexes.models import ActualVegIndex


class ProductivityClass(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Класс продуктивности'
        verbose_name_plural = "Классы продуктивности"


class ContourAverageIndex(models.Model):
    contour = models.ForeignKey('gip.ContourYear', on_delete=models.CASCADE, verbose_name='Контуры Поля')
    value = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        verbose_name='Средий показатель индекса',
        blank=True
    )
    productivity_class = models.ForeignKey(
        'indexes.ProductivityClass',
        on_delete=models.CASCADE,
        verbose_name='Класс продуктивности'
    )
    start_day = models.DateField(verbose_name='Начало периода')
    end_day = models.DateField(verbose_name='Конец периода')
    history = HistoricalRecords(verbose_name="История")
    index_count = models.IntegerField(verbose_name='Колличество индексов использованных для подсчёта')

    def __str__(self):
        return f'{self.contour}: {self.value}'

    class Meta:
        verbose_name = 'Средний индек контура'
        verbose_name_plural = "Средние индесы контуров"

    def save(self, *args, **kwargs):
        try:
            source = ActualVegIndex.objects.filter(contour=self.contour)
        except ValueError:
            return 'Data base have no Vegetation index'
        self.index_count = len(source)
        value = []
        date = []
        for i in source:
            value.append(i.average_value)
            date.append(i.date)
        self.value = (sum(value)) / self.index_count
        sorted_date = sorted(date)
        self.start_day = sorted_date[0]
        self.end_day = sorted_date[-1]

        super(ContourAverageIndex, self).save(*args, **kwargs)
