import glob
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import matplotlib.pyplot as plt
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from osgeo import gdal

from culture_model.models import VegetationIndex
from gip.models import Contour
from indexes.index_funcs import cutting_tiff
from indexes.index_funcs.ndmi_funcs import average_ndmi, ndmi_calculator
from indexes.index_funcs.ndre_funcs import average_ndre, ndre_calculator
from indexes.index_funcs.ndvi_funcs import average_ndvi, ndvi_calculator
from indexes.index_funcs.ndwi_funcs import average_ndwi, ndwi_calculator
from indexes.index_funcs.savi_funcs import average_savi, savi_calculator
from indexes.index_funcs.vari_funcs import average_vari, vari_calculator
from indexes.models import ActualVegIndex, IndexCreatingReport, IndexMeaning
from indexes.models import SciHubImageDate


def veg_index_creating(image_date):
    try:
        contours = Contour.objects.filter(polygon__coveredby=image_date.polygon)
        for contour in contours:
            polygon = GEOSGeometry(contour.polygon).geojson
            file_name = f'temporary file {datetime.now()}'
            output_path_b02 = f"./media/B02_{file_name}.tiff"
            output_path_b03 = f"./media/B03_{file_name}.tiff"
            output_path_b04 = f"./media/B04_{file_name}.tiff"
            output_path_b07 = f"./media/B07_{file_name}.tiff"
            output_path_b8a = f"./media/B8A_{file_name}.tiff"
            output_path_b11 = f"./media/B11_{file_name}.tiff"

            input_path_b02 = f'./media/{image_date.B02}'
            input_path_b03 = f'./media/{image_date.B03}'
            input_path_b04 = f'./media/{image_date.B04}'
            input_path_b07 = f'./media/{image_date.B07}'
            input_path_b8a = f'./media/{image_date.B8A}'
            input_path_b11 = f'./media/{image_date.B11}'
            gdal.UseExceptions()
            cutting_error = []

            try:
                cutting_tiff(outputpath=output_path_b02, inputpath=input_path_b02, polygon=polygon)
            except Exception as b02_error:
                cutting_error.append(f'B02 layer cutting error {b02_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b03, inputpath=input_path_b03, polygon=polygon)
            except Exception as b03_error:
                cutting_error.append(f'B03 layer cutting error cutting error {b03_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b04, inputpath=input_path_b04, polygon=polygon)
            except Exception as b04_error:
                cutting_error.append(f'B04 layer cutting error {b04_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b07, inputpath=input_path_b07, polygon=polygon)
            except Exception as b07_error:
                cutting_error.append(f'B07 layer cutting error {b07_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b8a, inputpath=input_path_b8a, polygon=polygon)
            except Exception as b8a_error:
                cutting_error.append(f'B8A layer cutting error {b8a_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b11, inputpath=input_path_b11, polygon=polygon)
            except Exception as b11_error:
                cutting_error.append(f'B11 layer cutting error {b11_error}')

            for veg_index in VegetationIndex.objects.all():
                if IndexCreatingReport.objects.filter(veg_index=veg_index, contour=contour, satellite_image=image_date):
                    pass
                else:
                    if IndexCreatingReport.objects.filter(
                            contour_id=contour.id,
                            is_processed=True,
                            satellite_image=image_date,
                            veg_index=veg_index
                    ):
                        pass
                    else:
                        try:
                            if veg_index.name == 'NDVI':
                                average_value = average_ndvi(red_file=output_path_b04, nir_file=output_path_b8a)

                                result_to_save = ndvi_calculator(
                                    B04=output_path_b04,
                                    B08=output_path_b8a,
                                    saving_file_name=file_name
                                )

                            elif veg_index.name == 'NDMI':
                                average_value = average_ndmi(swir_file=output_path_b11, nir_file=output_path_b8a)

                                result_to_save = ndmi_calculator(
                                    B11=output_path_b11,
                                    B08=output_path_b8a,
                                    saving_file_name=file_name
                                )

                            elif veg_index.name == 'NDWI':
                                average_value = average_ndwi(green_file=output_path_b03, nir_file=output_path_b8a)

                                result_to_save = ndwi_calculator(
                                    B03=output_path_b03,
                                    B08=output_path_b8a,
                                    saving_file_name=file_name
                                )
                            elif veg_index.name == 'NDRE':
                                average_value = average_ndre(red_file=output_path_b07, nir_file=output_path_b8a)

                                result_to_save = ndre_calculator(
                                    B07=output_path_b07,
                                    B8A=output_path_b8a,
                                    saving_file_name=file_name
                                )
                            elif veg_index.name == 'SAVI':
                                average_value = average_savi(red_file=output_path_b04, nir_file=output_path_b8a)

                                result_to_save = savi_calculator(
                                    B04=output_path_b04,
                                    B08=output_path_b8a,
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
                                    _('Ошибка создания индекса растительности, проверьте имена индексов'))
                            meaning_of_average_value = IndexMeaning.objects.filter(
                                index=veg_index
                            ).filter(
                                min_index_value__lt=average_value
                            ).filter(
                                max_index_value__gte=average_value
                            ).first()

                            actual = ActualVegIndex.objects.create(
                                average_value=average_value,
                                meaning_of_average_value=meaning_of_average_value,
                                contour_id=contour.id,
                                index_id=veg_index.id,
                                date=image_date.date
                            )
                            actual.index_image.save(f'{file_name}.png', result_to_save)

                            IndexCreatingReport.objects.create(
                                contour_id=contour.id,
                                veg_index_id=veg_index.id,
                                satellite_image_id=image_date.id,
                                is_processed=True,
                                process_error='No error'
                            )
                        except Exception as e:
                            plt.close()
                            # creating report
                            IndexCreatingReport.objects.create(
                                contour_id=contour.id,
                                veg_index_id=veg_index.id,
                                satellite_image_id=image_date.id,
                                is_processed=False,
                                process_error=f'{e}, {cutting_error}'
                            )

                        # Search files with .tiff extension in current directory
                    pattern = "./media/*.tiff"
                    files = glob.glob(pattern)

                    # deleting the files with tiff extension
                    for file in files:
                        os.remove(file)

    except Exception as e:
        print(e)
        IndexCreatingReport.objects.create(
            contour_id=None,
            veg_index_id=None,
            satellite_image_id=image_date.id,
            is_processed=False,
            process_error=f'Have no contours in this satellite image. Error is - {e}'
        )
        pass


def create_veg_indexes():
    image_dates = SciHubImageDate.objects.all()

    with ThreadPoolExecutor(max_workers=40) as executor:
        executor.map(veg_index_creating, image_dates)


def creating_veg_index_to_given_image(satellite_image):
    contours = Contour.objects.filter(polygon__coveredby=satellite_image.polygon)

    for contour in contours:
        polygon = GEOSGeometry(contour.polygon).geojson
        file_name = f'temporary file {datetime.now()}'
        output_path_b02 = f"./media/B02_{file_name}.tiff"
        output_path_b03 = f"./media/B03_{file_name}.tiff"
        output_path_b04 = f"./media/B04_{file_name}.tiff"
        output_path_b07 = f"./media/B07_{file_name}.tiff"
        output_path_b8a = f"./media/B8A_{file_name}.tiff"
        output_path_b11 = f"./media/B11_{file_name}.tiff"

        input_path_b02 = f'./media/{satellite_image.B02}'
        input_path_b03 = f'./media/{satellite_image.B03}'
        input_path_b04 = f'./media/{satellite_image.B04}'
        input_path_b07 = f'./media/{satellite_image.B07}'
        input_path_b8a = f'./media/{satellite_image.B8A}'
        input_path_b11 = f'./media/{satellite_image.B11}'
        gdal.UseExceptions()
        cutting_error = []

        try:
            cutting_tiff(outputpath=output_path_b02, inputpath=input_path_b02, polygon=polygon)
        except Exception as b02_error:
            cutting_error.append(f'B02 layer cutting error {b02_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b03, inputpath=input_path_b03, polygon=polygon)
        except Exception as b03_error:
            cutting_error.append(f'B03 layer cutting error cutting error {b03_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b04, inputpath=input_path_b04, polygon=polygon)
        except Exception as b04_error:
            cutting_error.append(f'B04 layer cutting error {b04_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b07, inputpath=input_path_b07, polygon=polygon)
        except Exception as b07_error:
            cutting_error.append(f'B07 layer cutting error {b07_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b8a, inputpath=input_path_b8a, polygon=polygon)
        except Exception as b8a_error:
            cutting_error.append(f'B8A layer cutting error {b8a_error}, ')
        try:
            cutting_tiff(outputpath=output_path_b11, inputpath=input_path_b11, polygon=polygon)
        except Exception as b11_error:
            cutting_error.append(f'B11 layer cutting error {b11_error}')

        for veg_index in VegetationIndex.objects.all():
            if IndexCreatingReport.objects.filter(veg_index=veg_index, contour=contour,
                                                  satellite_image=satellite_image):
                pass
            else:
                if IndexCreatingReport.objects.filter(
                        contour_id=contour.id,
                        is_processed=True,
                        satellite_image=satellite_image,
                        veg_index=veg_index
                ):

                    pass
                else:
                    try:
                        if veg_index.name == 'NDVI':
                            average_value = average_ndvi(red_file=output_path_b04, nir_file=output_path_b8a)

                            result_to_save = ndvi_calculator(
                                B04=output_path_b04,
                                B08=output_path_b8a,
                                saving_file_name=file_name
                            )

                        elif veg_index.name == 'NDMI':
                            average_value = average_ndmi(swir_file=output_path_b11, nir_file=output_path_b8a)

                            result_to_save = ndmi_calculator(
                                B11=output_path_b11,
                                B08=output_path_b8a,
                                saving_file_name=file_name
                            )

                        elif veg_index.name == 'NDWI':
                            average_value = average_ndwi(green_file=output_path_b03, nir_file=output_path_b8a)

                            result_to_save = ndwi_calculator(
                                B03=output_path_b03,
                                B08=output_path_b8a,
                                saving_file_name=file_name
                            )
                        elif veg_index.name == 'NDRE':
                            average_value = average_ndre(red_file=output_path_b07, nir_file=output_path_b8a)

                            result_to_save = ndre_calculator(
                                B07=output_path_b07,
                                B8A=output_path_b8a,
                                saving_file_name=file_name
                            )
                        elif veg_index.name == 'SAVI':
                            average_value = average_savi(red_file=output_path_b04, nir_file=output_path_b8a)

                            result_to_save = savi_calculator(
                                B04=output_path_b04,
                                B08=output_path_b8a,
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
                                _('Ошибка создания индекса растительности, проверьте имена индексов'))
                        meaning_of_average_value = IndexMeaning.objects.filter(
                            index=veg_index
                        ).filter(
                            min_index_value__lt=average_value
                        ).filter(
                            max_index_value__gte=average_value
                        ).first()

                        actual = ActualVegIndex.objects.create(
                            average_value=average_value,
                            meaning_of_average_value=meaning_of_average_value,
                            contour_id=contour.id,
                            index_id=veg_index.id,
                            date=satellite_image.date
                        )
                        actual.index_image.save(f'{file_name}.png', result_to_save)

                        IndexCreatingReport.objects.create(
                            contour_id=contour.id,
                            veg_index_id=veg_index.id,
                            satellite_image_id=satellite_image.id,
                            is_processed=True,
                            process_error='No error'
                        )
                    except Exception as e:
                        plt.close()
                        # creating report
                        IndexCreatingReport.objects.create(
                            contour_id=contour.id,
                            veg_index_id=veg_index.id,
                            satellite_image_id=satellite_image.id,
                            is_processed=False,
                            process_error=f'{e}, {cutting_error}'
                        )

        # Search files with .tiff extension in current directory
        pattern = "./media/*.tiff"
        files = glob.glob(pattern)

        # deleting the files with tiff extension
        for file in files:
            os.remove(file)
