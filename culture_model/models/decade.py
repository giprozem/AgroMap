from django.contrib.gis.db import models


class Decade(models.Model):
    start_date = models.DateField(verbose_name='From')
    end_date = models.DateField(verbose_name='To')

    class Meta:
        verbose_name = 'Decade'
        verbose_name_plural = "Decades"

    def __str__(self):
        return f"с {self.start_date} по {self.end_date}"
