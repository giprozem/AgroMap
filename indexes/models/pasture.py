from django.contrib.gis.db import models
from simple_history.models import HistoricalRecords
from django.utils.translation import gettext_lazy as _
from indexes.models import ActualVegIndex


class ProductivityClass(models.Model):

    """
    The ProductivityClass model is designed to represent categories or classes related to productivity. 
    It provides a way to define different productivity classes, each with a name and an optional description.
    """

    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Productivity Class')
        verbose_name_plural = _("Productivity Classes")


class ContourAverageIndex(models.Model):

    """
    The ContourAverageIndex model is designed to calculate and store the average index values for specific contours. 
    It provides fields to link to a contour, store the calculated average value, associate a productivity class, 
    specify the start and end date of the calculation period, and keep a historical record of changes.
    """
    
    contour = models.ForeignKey('gip.Contour', on_delete=models.CASCADE, verbose_name=_('Field Contours'))
    value = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        verbose_name=_('Average Index Value'),
        blank=True
    )
    productivity_class = models.ForeignKey(
        'indexes.ProductivityClass',
        on_delete=models.CASCADE,
        verbose_name=_('Productivity Class')
    )
    start_day = models.DateField(verbose_name=_('Start Date'))
    end_day = models.DateField(verbose_name=_('End Date'))
    history = HistoricalRecords(verbose_name=_("History"))
    index_count = models.IntegerField(verbose_name=_('Number of Indices Used for Calculation'))

    def __str__(self):
        return f'{self.contour}: {self.value}'

    class Meta:
        verbose_name = _('Contour Average Index')
        verbose_name_plural = _("Contour Average Indices")

    def save(self, *args, **kwargs):
        try:
            source = ActualVegIndex.objects.filter(contour=self.contour)
        except ValueError:
            return 'Database has no Vegetation index'
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
