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
from indexes.index_funcs.ndvi_funcs import average_ndvi, ndvi_calculator
from indexes.index_funcs.ndwi_funcs import average_ndwi, ndwi_calculator
from indexes.index_funcs.ndre_funcs import average_ndre, ndre_calculator
from indexes.index_funcs.common_funcs import cutting_tiff
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
    contour = models.ForeignKey('gip.ContourYear', on_delete=models.CASCADE, verbose_name='Контуры Поля')
    date = models.DateField(verbose_name='Дата анализа', help_text='Введите дату космо снимка из которого будет высчитан индекс')
    history = HistoricalRecords(verbose_name="История")

    def __str__(self):
        return f'{self.index} {self.contour}'

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

        file_name = f'время сохранения {datetime.datetime.now()}'

        polygon = GEOSGeometry(self.contour.polygon).geojson

        output_path_b03 = f"./media/B03_{file_name}.tiff"
        output_path_b04 = f"./media/B04_{file_name}.tiff"
        output_path_b07 = f"./media/B07_{file_name}.tiff"
        output_path_b8a = f"./media/B8A_{file_name}.tiff"
        output_path_b08 = f"./media/B08_{file_name}.tiff"
        output_path_b11 = f"./media/B11_{file_name}.tiff"

        input_path_b03 = f'./media/{source.B03}'
        input_path_b04 = f'./media/{source.B04}'
        input_path_b07 = f'./media/{source.B07}'
        input_path_b8a = f'./media/{source.B8A}'
        input_path_b08 = f'./media/{source.B08}'
        input_path_b11 = f'./media/{source.B11}'

        cutting_tiff(outputpath=output_path_b03, inputpath=input_path_b03, polygon=polygon)
        cutting_tiff(outputpath=output_path_b04, inputpath=input_path_b04, polygon=polygon)
        cutting_tiff(outputpath=output_path_b07, inputpath=input_path_b07, polygon=polygon)
        cutting_tiff(outputpath=output_path_b8a, inputpath=input_path_b8a, polygon=polygon)
        cutting_tiff(outputpath=output_path_b08, inputpath=input_path_b08, polygon=polygon)
        cutting_tiff(outputpath=output_path_b11, inputpath=input_path_b11, polygon=polygon)

        if self.index.name == 'NDVI':
            self.average_value = average_ndvi(red_file=output_path_b04, nir_file=output_path_b08)

            ndvi_calculator(B04=output_path_b04, B08=output_path_b08, saving_file_name=file_name)

        elif self.index.name == 'NDMI':
            self.average_value = average_ndmi(swir_file=output_path_b11, nir_file=output_path_b08)

            ndmi_calculator(B11=output_path_b11, B08=output_path_b08, saving_file_name=file_name)

        elif self.index.name == 'NDWI':
            self.average_value = average_ndwi(green_file=output_path_b03, nir_file=output_path_b8a)

            ndwi_calculator(B03=output_path_b03, B08=output_path_b8a, saving_file_name=file_name)
        elif self.index.name == 'NDRE':
            self.average_value = average_ndre(red_file=output_path_b07, nir_file=output_path_b8a)

            ndre_calculator(B07=output_path_b07, B8A=output_path_b8a, saving_file_name=file_name)

        else:
            raise ObjectDoesNotExist(_('Data base have no satellite images that have to process'))
        self.meaning_of_average_value = IndexMeaning.objects.filter(
            index=self.index
        ).filter(
            min_index_value__lt=self.average_value
        ).filter(
            max_index_value__gte=self.average_value
        ).first()
        path = Path(f'./media/{file_name}.png')
        with path.open(mode='rb') as f:
            image = File(f, name=path.name)
            self.index_image = image
            super(ActuaVegIndex, self).save(*args, **kwargs)

        self.remove_file(output_path_b03)
        self.remove_file(output_path_b04)
        self.remove_file(output_path_b07)
        self.remove_file(output_path_b08)
        self.remove_file(output_path_b8a)
        self.remove_file(output_path_b11)
        self.remove_file(f'./media/{file_name}.png')


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
