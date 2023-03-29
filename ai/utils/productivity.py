import datetime
import glob
import os

import matplotlib.pyplot as plt
from django.contrib.gis.geos import GEOSGeometry
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from osgeo import gdal
from rest_framework.renderers import JSONRenderer

from ai.models.predicted_contour import Contour_AI
from ai.productivity_funcs.training import predict, model_path
from ai.serializers import ContourAIStatisticsSerializer
from culture_model.models import VegetationIndex
from indexes.index_funcs import cutting_tiff, average_ndvi, ndvi_calculator, average_ndmi, ndmi_calculator, \
    average_ndre, ndre_calculator, average_savi, savi_calculator, average_vari, vari_calculator
from indexes.index_funcs.ndwi_funcs import average_ndwi, ndwi_calculator
from indexes.models import SciHubImageDate, ContourAIIndexCreatingReport, IndexMeaning, PredictedContourVegIndex


def predicting_productivity(contour_ai_id):
    response = Contour_AI.objects.get(id=contour_ai_id)
    serializer = ContourAIStatisticsSerializer(response)
    res = [serializer.data]
    json_data = JSONRenderer().render(res)
    json_string = json_data.decode('utf-8')
    result = predict(model_path=model_path, predict_path=json_string)
    print(result)
    if result == 0:
        response.productivity = '0 - 1.6'
    elif result == 1:
        response.productivity = '1.6 - 5'
    elif result == 2:
        response.productivity = '5 - 10'
    elif result == 3:
        response.productivity = '10 - 15'
    elif result == 4:
        response.productivity = '15 - 20'
    elif result == 5:
        response.productivity = '25 - 30'
    elif result == 6:
        response.productivity = '30 - 35'
    elif result == 7:
        response.productivity = '35 - 40'
    elif result == 8:
        response.productivity = '40 - 45'
    elif result == 1:
        response.productivity = '45 - 50'
    elif result == 1:
        response.productivity = '50 - 55'
    response.save()


def creating_veg_indexes():
    image_dates = SciHubImageDate.objects.all()
    for image_date in image_dates:
        contours = Contour_AI.objects.filter(polygon__coveredby=image_date.polygon)
        for contour in contours:
            polygon = GEOSGeometry(contour.polygon).geojson
            file_name = f'temporary file {datetime.datetime.now()}'
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
                if ContourAIIndexCreatingReport.objects.filter(veg_index=veg_index, contour=contour, satellite_image=image_date):
                    pass
                else:
                    if ContourAIIndexCreatingReport.objects.filter(
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

                            actual = PredictedContourVegIndex.objects.create(
                                average_value=average_value,
                                meaning_of_average_value=meaning_of_average_value,
                                contour_id=contour.id,
                                index_id=veg_index.id,
                                date=image_date.date
                            )
                            actual.index_image.save(f'{file_name}.png', result_to_save)

                            ContourAIIndexCreatingReport.objects.create(
                                contour_id=contour.id,
                                veg_index_id=veg_index.id,
                                satellite_image_id=image_date.id,
                                is_processed=True,
                                process_error='No error'
                            )
                        except Exception as e:
                            plt.close()
                            # creating report
                            ContourAIIndexCreatingReport.objects.create(
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
