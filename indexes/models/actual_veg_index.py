import datetime
import os
from pathlib import Path

from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from indexes.index_funcs.ndmi_funcs import average_ndmi, ndmi_calculator
from indexes.index_funcs.ndvi_funcs import cutting_tiff, average_ndvi, ndvi_calculator
from indexes.models.satelliteimage import SatelliteImages


class ActuaVegIndex(models.Model):
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
    contour = models.ForeignKey('gip.Contour', on_delete=models.CASCADE, verbose_name='Контуры Поля')
    date = models.DateField(verbose_name='Дата анализа', help_text='Введите дату космо снимка из которого будет высчитан индекс')
    history = HistoricalRecords(verbose_name="История")

    def __str__(self):
        return f'{self.index} {self.contour.ink}'

    class Meta:
        verbose_name = 'Фактический Индекс'
        verbose_name_plural = "Фактические Индексы"

    def remove_file(self, deleting_path):
        if os.path.isfile(deleting_path):
            os.remove(deleting_path)

    def save(self, *args, **kwargs):
        source = SatelliteImages.objects.filter(date=self.date).first()

        if source == None:
            # TODO refactor the response
            raise ObjectDoesNotExist('Data base have no satellite images that have to process')

        file_name = self.contour.ink + f'время сохранения {datetime.datetime.now()}'

        polygon = GEOSGeometry(self.contour.polygon).geojson

        if self.index.name == 'NDVI':
            output_path_B04 = f"./media/B04_{file_name}.tiff"
            input_path_B04 = f'./media/{source.B04}'
            output_path_B8A = f"./media/B8A_{file_name}.tiff"
            input_path_B8A = f'./media/{source.B8A}'
            cutting_tiff(outputpath=output_path_B04, inputpath=input_path_B04, polygon=polygon)
            cutting_tiff(outputpath=output_path_B8A, inputpath=input_path_B8A, polygon=polygon)
            self.average_value = average_ndvi(red_file=output_path_B04, nir_file=output_path_B8A)

            self.meaning_of_average_value = IndexMeaning.objects.filter(
                index=self.index
            ).filter(
                min_index_value__lt=self.average_value
            ).filter(
                max_index_value__gte=self.average_value
            ).first()
            # TODO code is repeating
            ndvi_calculator(B04=output_path_B04, B8A=output_path_B8A, saving_file_name=file_name)

            self.remove_file(output_path_B04)
            self.remove_file(output_path_B8A)

            path = Path(f'./media/{file_name}.png')
            with path.open(mode='rb') as f:
                image = File(f, name=path.name)

                self.index_image = image
                self.remove_file(f'./media/{file_name}.png')
                super(ActuaVegIndex, self).save(*args, **kwargs)
        elif self.index.name == 'NDMI':
            output_path_B11 = f"./media/B11_{file_name}.tiff"
            input_path_B11 = f'./media/{source.B11}'
            output_path_B08 = f"./media/B08_{file_name}.tiff"
            input_path_B08 = f'./media/{source.B08}'
            cutting_tiff(outputpath=output_path_B11, inputpath=input_path_B11, polygon=polygon)
            cutting_tiff(outputpath=output_path_B08, inputpath=input_path_B08, polygon=polygon)
            self.average_value = average_ndmi(swir_file=output_path_B11, nir_file=output_path_B08)

            self.meaning_of_average_value = IndexMeaning.objects.filter(
                index=self.index
            ).filter(
                min_index_value__lt=self.average_value
            ).filter(
                max_index_value__gte=self.average_value
            ).first()
            # TODO code is repeating

            ndmi_calculator(B11=output_path_B11, B08=output_path_B08, saving_file_name=file_name)

            self.remove_file(output_path_B11)
            self.remove_file(output_path_B08)

            path = Path(f'./media/{file_name}.png')
            with path.open(mode='rb') as f:
                image = File(f, name=path.name)

                self.index_image = image
                self.remove_file(f'./media/{file_name}.png')
                super(ActuaVegIndex, self).save(*args, **kwargs)
        else:
            raise ObjectDoesNotExist(_('Data base have no satellite images that have to process'))


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
