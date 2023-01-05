from django.contrib.gis.db import models


class Decade(models.Model):
    start_date = models.DateField(verbose_name='с')
    end_date = models.DateField(verbose_name='по')

    class Meta:
        verbose_name = 'Декада'
        verbose_name_plural = "Декады"

    def __str__(self):
        return f"с {self.start_date} по {self.end_date}"
