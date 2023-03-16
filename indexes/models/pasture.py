from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from indexes.models import ActualVegIndex


class ProductivityClass(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Класс продуктивности')
        verbose_name_plural = _("Классы продуктивности")


class ContourAverageIndex(models.Model):
    contour = models.ForeignKey('gip.Contour', on_delete=models.CASCADE, verbose_name=_('Контуры поля'))
    value = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        verbose_name=_('Средний показатель индекса'),
        blank=True
    )
    productivity_class = models.ForeignKey(
        'indexes.ProductivityClass',
        on_delete=models.CASCADE,
        verbose_name=_('Класс продуктивности')
    )
    start_day = models.DateField(verbose_name=_('Начало периода'))
    end_day = models.DateField(verbose_name=_('Конец периода'))
    history = HistoricalRecords(verbose_name=_("История"))
    index_count = models.IntegerField(verbose_name=_('Колличество индексов использованных для подсчёта'))

    def __str__(self):
        return f'{self.contour}: {self.value}'

    class Meta:
        verbose_name = _('Средний индекc контура')
        verbose_name_plural = _("Средние индексы контуров")

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
