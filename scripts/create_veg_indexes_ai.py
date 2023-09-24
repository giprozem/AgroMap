"""
This module provides functionality to create vegetation indices for satellite images.
These indices help in understanding the health and density of vegetation in a particular region.
"""

import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial

import matplotlib.pyplot as plt
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from osgeo import gdal

from ai.models.predicted_contour import Contour_AI
from culture_model.models import VegetationIndex
from indexes.index_funcs import cutting_tiff
from indexes.index_funcs.ndvi_funcs import average_ndvi, ndvi_calculator
from indexes.index_funcs.ndwi_funcs import average_ndwi, ndwi_calculator
from indexes.index_funcs.savi_funcs import average_savi, savi_calculator
from indexes.index_funcs.vari_funcs import average_vari, vari_calculator
from indexes.models import IndexMeaning
from indexes.models import PredictedContourVegIndex, ContourAIIndexCreatingReport
from indexes.models.satelliteimage import SciHubImageDate


def remove_file(file_path):
    """
        Remove a file from the filesystem if it exists.

        Parameters:
    -    - file_path (str): The path of the file to be deleted.
    """
    if os.path.isfile(file_path):
        os.remove(file_path)


def veg_index_creating(satellite_image, contour_obj, creating_report_obj, veg_index_obj):
    """
        Create vegetation indices for a given satellite image and store them in the database.
        It also generates reports of successful and unsuccessful index creations.

        Parameters:
        - satellite_image (Model instance): The satellite image to be processed.
        - contour_obj (Django Model): The model representing the contours of interest.
        - creating_report_obj (Django Model): The model used for storing processing reports.
        - veg_index_obj (Django Model): The model representing vegetation index values.
    """
    # Fetch contours that are covered by the given satellite image.
    contours = contour_obj.objects.filter(polygon__coveredby=satellite_image.polygon)
    try:
        for contour in contours:
            # Extracting the geojson representation of the contour's polygon.
            polygon = GEOSGeometry(contour.polygon).geojson

            # Generating file names for different spectral bands of the satellite image.
            file_name = f'temporary_file_{contour.id}-satellite_image-{satellite_image.id}'
            output_path_tcl = f"./media/TCL_{file_name}.tiff"
            output_path_b02 = f"./media/B02_{file_name}.tiff"
            output_path_b03 = f"./media/B03_{file_name}.tiff"
            output_path_b04 = f"./media/B04_{file_name}.tiff"
            output_path_b08 = f"./media/B08_{file_name}.tiff"
            gdal.UseExceptions()

            # List to capture errors during cutting operations.
            cutting_error = []

            # Attempt to cut each spectral band based on the contour's polygon.
            try:
                cutting_tiff(
                    outputpath=output_path_b02,
                    inputpath=f".{satellite_image.B02.url.replace('mediafiles', 'media')}",
                    polygon=polygon
                )
            except Exception as b02_error:
                cutting_error.append(f'B02 layer cutting error {b02_error}, ')  # TODO Required translate
            try:
                cutting_tiff(
                    outputpath=output_path_b03,
                    inputpath=f".{satellite_image.B03.url.replace('mediafiles', 'media')}",
                    polygon=polygon
                )
            except Exception as b03_error:
                cutting_error.append(f'B03 layer cutting error cutting error {b03_error}, ')  # TODO Required translate
            try:
                cutting_tiff(
                    outputpath=output_path_b04,
                    inputpath=f".{satellite_image.B04.url.replace('mediafiles', 'media')}",
                    polygon=polygon
                )
            except Exception as b04_error:
                cutting_error.append(f'B04 layer cutting error {b04_error}, ')  # TODO Required translate
            try:
                cutting_tiff(
                    outputpath=output_path_b08,
                    inputpath=f".{satellite_image.B8A.url.replace('mediafiles', 'media')}",
                    polygon=polygon
                )
            except Exception as b08_error:
                cutting_error.append(f'B08 layer cutting error {b08_error}, ')
            for veg_index in VegetationIndex.objects.all():
                if veg_index_obj.objects.filter(
                        index=veg_index,
                        contour=contour,
                ):
                    pass
                else:
                    try:
                        print(f'try index {veg_index.id} {contour.id}')
                        if veg_index.name == 'NDVI':
                            average_value = average_ndvi(red_file=output_path_b04, nir_file=output_path_b08)
                            result_to_save = ndvi_calculator(
                                B04=output_path_b04,
                                B08=output_path_b08,
                                saving_file_name=file_name
                            )
                        elif veg_index.name == 'NDWI':
                            average_value = average_ndwi(green_file=output_path_b03,
                                                         nir_file=output_path_b08)
                            result_to_save = ndwi_calculator(
                                B03=output_path_b03,
                                B08=output_path_b08,
                                saving_file_name=file_name
                            )
                        elif veg_index.name == 'SAVI':
                            average_value = average_savi(red_file=output_path_b04, nir_file=output_path_b08)
                            result_to_save = savi_calculator(
                                B04=output_path_b04,
                                B08=output_path_b08,
                                saving_file_name=file_name
                            )
                        elif veg_index.name == 'VARI':
                            average_value = average_vari(
                                red_file=output_path_b04,
                                green_file=output_path_b03,
                                blue_file=output_path_b02
                            )
                            result_to_save = vari_calculator(
                                B02=output_path_b02,
                                B03=output_path_b03,
                                B04=output_path_b04,
                                saving_file_name=file_name
                            )
                        else:
                            raise ObjectDoesNotExist(
                                _('Error creating vegetation index, check index names'))
                        meaning_of_average_value = IndexMeaning.objects.filter(
                            index=veg_index
                        ).filter(
                            min_index_value__lt=average_value
                        ).filter(
                            max_index_value__gte=average_value
                        ).first()
                        actual = veg_index_obj.objects.create(
                            average_value=average_value,
                            meaning_of_average_value=meaning_of_average_value,
                            contour_id=contour.id,
                            index_id=veg_index.id,
                            date=satellite_image.date,
                        )
                        actual.index_image.save(f'{file_name}.png', result_to_save)
                        creating_report_obj.objects.create(
                            contour_id=contour.id,
                            is_processed=True,
                            process_error='No error'  # TODO Required translate
                        )
                    except Exception as e:
                        plt.close()
                        creating_report_obj.objects.create(
                            contour_id=contour.id,
                            veg_index_id=veg_index.id,
                            is_processed=False,
                            process_error=f'{e}, {cutting_error}'
                        )

            # Removing all the temporary files created during the process.
            remove_file(output_path_b02)
            remove_file(output_path_b03)
            remove_file(output_path_b04)
            remove_file(output_path_b08)
            remove_file(output_path_tcl)
    except Exception as er:
        print(er)


def run():
    """
        Process all satellite images in the database to create vegetation indices using a thread pool.
    """

    # Fetch all satellite images.
    satellite_images = SciHubImageDate.objects.all()

    # Partially initialize the veg_index_creating function with common arguments.
    veg_index_creating_preset = partial(
        veg_index_creating,
        contour_obj=Contour_AI,
        creating_report_obj=ContourAIIndexCreatingReport,
        veg_index_obj=PredictedContourVegIndex
    )

    # Use ThreadPoolExecutor to process images concurrently.
    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(veg_index_creating_preset, satellite_images)
