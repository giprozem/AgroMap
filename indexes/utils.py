import matplotlib.pyplot as plt
import numpy as np
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from osgeo import gdal

from culture_model.models import VegetationIndex
from gip.models import Contour
from indexes.index_funcs import cutting_tiff
from indexes.index_funcs.ndvi_funcs import average_ndvi, ndvi_calculator
from indexes.index_funcs.ndwi_funcs import average_ndwi, ndwi_calculator
from indexes.index_funcs.savi_funcs import average_savi, savi_calculator
from indexes.index_funcs.vari_funcs import average_vari, vari_calculator
from indexes.models import IndexMeaning

import os
import cv2


def remove_file(file_path):
    """
        Remove a file from the filesystem if it exists.

        Parameters:
    -    - file_path (str): The path of the file to be deleted.
    """
    if os.path.isfile(file_path):
        os.remove(file_path)


def veg_index_creating(satellite_image, creating_report_obj, veg_index_obj, contour_obj):
    """
    This function is designed to process a given satellite image, extract various vegetation indices for specified contours,
    and save the processed results along with any errors encountered during processing.

    Parameters:
    - satellite_image: A satellite image object that covers a certain geographical area and contains various spectral bands.
    - contour_obj: Contour model that represents geographical boundaries.
    - creating_report_obj: Model for logging the processing reports, including any errors.
    - veg_index_obj: Vegetation index model used to store the computed vegetation index values.
    """
    contours = Contour.objects.filter(polygon__coveredby=satellite_image.polygon, id=contour_obj)
    # Beginning of main processing. Exception handling is used extensively to log errors in the processing report.
    try:
        for contour in contours:
            # Convert the contour's polygon into GeoJSON format.
            polygon = GEOSGeometry(contour.polygon).geojson
            # Constructing the unique file name for each contour and satellite image pair.
            file_name = f'temporary_file_{contour.id}-satellite_image-{satellite_image.id}'
            # Specifying the paths where the clipped satellite images for different bands will be saved.
            output_path_tcl = f"./media/TCL_{file_name}.tiff"
            output_path_b02 = f"./media/B02_{file_name}.tiff"
            output_path_b03 = f"./media/B03_{file_name}.tiff"
            output_path_b04 = f"./media/B04_{file_name}.tiff"
            output_path_b08 = f"./media/B08_{file_name}.tiff"

            # GDAL is used for geospatial operations, and we set it to raise Python exceptions for any errors.
            gdal.UseExceptions()
            tci_error = []

            # The following block tries to clip the satellite image's TCI band using the contour's polygon.
            # Errors in this process are captured and logged.
            try:
                cutting_tiff(
                    outputpath=output_path_tcl,
                    inputpath=f".{satellite_image.TCI.url.replace('mediafiles', 'media')}",
                    polygon=polygon
                )
                # The block below checks if more than 20% of the clipped TCI image is white (indicating clouds or snow).
                # If so, the process is aborted and the issue is logged.
                try:
                    image = cv2.imread(output_path_tcl, cv2.IMREAD_GRAYSCALE)
                    white = np.sum(image == 255)
                    size = image.shape[0] * image.shape[1]
                    percent = white / size * 100
                    if percent > 20:
                        # (Code related to processing the image and checking for white pixels)
                        creating_report_obj.objects.create(
                            contour_id=contour.id,
                            is_processed=False,
                            satellite_image=satellite_image,
                            process_error=f'In satellite image {percent}% snow or clouds. Or {tci_error}'
                        )
                    else:
                        # If the TCI image is valid, we proceed to clip the other spectral bands.
                        # Errors during this process are captured and logged.
                        cutting_error = []
                        try:
                            cutting_tiff(
                                outputpath=output_path_b02,
                                inputpath=f".{satellite_image.B02.url.replace('mediafiles', 'media')}",
                                polygon=polygon
                            )
                        except Exception as b02_error:
                            cutting_error.append(f'B02 layer cutting error {b02_error}, ')
                        try:
                            cutting_tiff(
                                outputpath=output_path_b03,
                                inputpath=f".{satellite_image.B03.url.replace('mediafiles', 'media')}",
                                polygon=polygon
                            )
                        except Exception as b03_error:
                            cutting_error.append(
                                f'B03 layer cutting error cutting error {b03_error}, ')
                        try:
                            cutting_tiff(
                                outputpath=output_path_b04,
                                inputpath=f".{satellite_image.B04.url.replace('mediafiles', 'media')}",
                                polygon=polygon
                            )
                        except Exception as b04_error:
                            cutting_error.append(f'B04 layer cutting error {b04_error}, ')
                        try:
                            cutting_tiff(
                                outputpath=output_path_b08,
                                inputpath=f".{satellite_image.B08.url.replace('mediafiles', 'media')}",
                                polygon=polygon
                            )

                        except Exception as b08_error:
                            cutting_error.append(f'B08 layer cutting error {b08_error}, ')
                        for veg_index in VegetationIndex.objects.all():
                            if veg_index_obj.objects.filter(
                                    index=veg_index,
                                    contour=contour,
                                    satellite_image=satellite_image,
                            ):
                                pass
                            else:
                                try:
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
                                        satellite_image=satellite_image
                                    )
                                    actual.index_image.save(f'{file_name}.png', result_to_save)
                                except Exception as e:
                                    plt.close()
                                    creating_report_obj.objects.create(
                                        contour_id=contour.id,
                                        veg_index_id=veg_index.id,
                                        satellite_image_id=satellite_image.id,
                                        is_processed=False,
                                        process_error=f'{e}, {cutting_error}'
                                    )
                except Exception as e:
                    creating_report_obj.objects.create(
                        contour_id=contour.id,
                        is_processed=False,
                        satellite_image=satellite_image,
                        process_error=f'In satellite image {percent}% snow or clouds. Or {e}'
                    )
            except gdal.UseExceptions() as tci_err:
                tci_error.append(tci_err)
            remove_file(output_path_b02)
            remove_file(output_path_b03)
            remove_file(output_path_b04)
            remove_file(output_path_b08)
            remove_file(output_path_tcl)
    except Exception as e:
        creating_report_obj.objects.create(
            contour_id=None,
            veg_index_id=None,
            satellite_image_id=satellite_image.id,
            is_processed=False,
            process_error=f'There is no satellite image. Error is - {e}')
