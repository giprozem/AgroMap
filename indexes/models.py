import datetime
import os
from pathlib import Path

from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator
from simple_history.models import HistoricalRecords

from gip.models.contour import Contour
from indexes.ndmi_funcs import average_ndmi, ndmi_calculator
from indexes.ndvi_funcs import cutting_tiff, average_ndvi, ndvi_calculator
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseBadRequest, Http404

DATE_OF_SATELLITE_IMAGES = (
    ('Весна', '04.05.2022 (Весна)'),
    ('Лето', '15.07.2022 (Лето)'),
    ('Осень', '25.09.2022 (Осень)'),

)


class NDVIIndex(models.Model):
    ndvi_image = models.FileField(upload_to='ndvi_png', blank=True, verbose_name='Картинка NDVI')
    history = HistoricalRecords(verbose_name="История")
    contour = models.ForeignKey(Contour, on_delete=models.SET_NULL, null=True, verbose_name='Контуры Поля')
    date_of_satellite_image = models.CharField(
        choices=DATE_OF_SATELLITE_IMAGES,
        verbose_name='Дата космоснимка',
        max_length=5)
    average_NDVI = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='Средий показатель NDVI', default=0)

    class Meta:
        verbose_name = 'Индекс NDVI'
        verbose_name_plural = "Индексы NDVI"

    def __str__(self):
        return self.contour.ink


class IndexFact(models.Model):
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
    decade = models.ForeignKey('culture_model.Decade', on_delete=models.CASCADE, verbose_name='Декада')
    index = models.ForeignKey('culture_model.Index', on_delete=models.CASCADE, verbose_name='Индекс')
    contour = models.ForeignKey('gip.Contour', on_delete=models.CASCADE, verbose_name='Контуры Поля')
    source = models.ForeignKey('indexes.SatelliteImages', on_delete=models.CASCADE, verbose_name='Источник')
    history = HistoricalRecords(verbose_name="История")

    def __str__(self):
        return f'{self.index} {self.contour.ink} {self.source.region_name}'

    class Meta:
        verbose_name = 'Фактический Индекс'
        verbose_name_plural = "Фактические Индексы"

    def remove_file(self, deleting_path):
        if os.path.isfile(deleting_path):
            os.remove(deleting_path)

    def save(self, *args, **kwargs):
        file_name = self.contour.ink + f'время сохранения {datetime.datetime.now()}'

        polygon = GEOSGeometry(self.contour.polygon).geojson

        if self.index.name == 'NDVI':
            output_path_B04 = f"./media/B04_{file_name}.tiff"
            input_path_B04 = f'./media/{self.source.B04}'
            output_path_B8A = f"./media/B8A_{file_name}.tiff"
            input_path_B8A = f'./media/{self.source.B8A}'
            cutting_tiff(outputpath=output_path_B04, inputpath=input_path_B04, polygon=polygon)
            cutting_tiff(outputpath=output_path_B8A, inputpath=input_path_B8A, polygon=polygon)
            self.average_value = average_ndvi(red_file=output_path_B04, nir_file=output_path_B8A)

            self.meaning_of_average_value = IndexMeaning.objects.filter(
                index=self.index
            ).filter(
                min_index_value__lte=self.average_value
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
                super(IndexFact, self).save(*args, **kwargs)
        elif self.index.name == 'NDMI':
            output_path_B11 = f"./media/B11_{file_name}.tiff"
            input_path_B11 = f'./media/{self.source.B11}'
            output_path_B08 = f"./media/B08_{file_name}.tiff"
            input_path_B08 = f'./media/{self.source.B08}'
            cutting_tiff(outputpath=output_path_B11, inputpath=input_path_B11, polygon=polygon)
            cutting_tiff(outputpath=output_path_B08, inputpath=input_path_B08, polygon=polygon)
            self.average_value = average_ndmi(swir_file=output_path_B11, nir_file=output_path_B08)

            self.meaning_of_average_value = IndexMeaning.objects.filter(
                index=self.index
            ).filter(
                min_index_value__lte=self.average_value
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
                super(IndexFact, self).save(*args, **kwargs)
        else:
            raise ObjectDoesNotExist(_('Data base have no satellite images that have to process'))


class SatelliteImages(models.Model):
    region_name = models.CharField(max_length=100, verbose_name='Название региона')
    description = models.TextField(null=True, blank=True, verbose_name='Описание', help_text='Заполняется при необходимости')
    date = models.DateField(verbose_name='дата снимков')
    B01 = models.FileField(upload_to='satellite_images', verbose_name='Слой B01', help_text='Coastal aerosol', blank=True, null=True)
    B02 = models.FileField(upload_to='satellite_images', verbose_name='Слой B02', help_text='Blue', blank=True, null=True)
    B03 = models.FileField(upload_to='satellite_images', verbose_name='Слой B03', help_text='Green', blank=True, null=True)
    B04 = models.FileField(upload_to='satellite_images', verbose_name='Слой B04', help_text='Red', blank=True, null=True)
    B05 = models.FileField(upload_to='satellite_images', verbose_name='Слой B05', help_text='Vegetation red edge', blank=True, null=True)
    B06 = models.FileField(upload_to='satellite_images', verbose_name='Слой B06', help_text='Vegetation red edge', blank=True, null=True)
    B07 = models.FileField(upload_to='satellite_images', verbose_name='Слой B07', help_text='Vegetation red edge', blank=True, null=True)
    B08 = models.FileField(upload_to='satellite_images', verbose_name='Слой B08', help_text='NIR', blank=True, null=True)
    B8A = models.FileField(upload_to='satellite_images', verbose_name='Слой B8A', help_text='Narrow NIR', blank=True, null=True)
    B09 = models.FileField(upload_to='satellite_images', verbose_name='Слой B09', help_text='Water vapour', blank=True, null=True)
    B10 = models.FileField(upload_to='satellite_images', verbose_name='Слой B10', help_text='SWIR – Cirrus', blank=True, null=True)
    B11 = models.FileField(upload_to='satellite_images', verbose_name='Слой B11', help_text='SWIR – 1', blank=True, null=True)
    B12 = models.FileField(upload_to='satellite_images', verbose_name='Слой B12', help_text='SWIR - 2', blank=True, null=True)
    history = HistoricalRecords(verbose_name="История")

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = 'Спутниковый снимок'
        verbose_name_plural = "Спутниковые снимки"


class IndexMeaning(models.Model):
    index = models.ForeignKey('culture_model.Index', on_delete=models.CASCADE, verbose_name='Индекс')
    min_index_value = models.DecimalField(max_digits=4, decimal_places=3, validators=[MinValueValidator(-1)], verbose_name='Минимальное значение')
    max_index_value = models.DecimalField(max_digits=4, decimal_places=3, validators=[MaxValueValidator(1)], verbose_name='Максимальное значение')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Значение показателя индекса'
        verbose_name_plural = "Значение показателей индексов"

    def __str__(self):
        return f'{self.index} {self.min_index_value} {self.max_index_value}'


