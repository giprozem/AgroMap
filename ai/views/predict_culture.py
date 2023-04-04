import datetime
import glob
import os

import torch
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.culture_AI.predict_culture import predict_from_raster_bands
from ai.models.predicted_contour import Contour_AI
from ai.serializers import Contour_AISerializer
from indexes.index_funcs import cutting_tiff
from indexes.models import SciHubImageDate
from osgeo import gdal


class CulturePredict(APIView):

    def get(self, request, *args, **kwargs):
        query = Contour_AI.objects.all()
        print(query[0].polygon)

        image_date = SciHubImageDate.objects.filter(id=request.query_params['satellite_id'])
        image_date = image_date[0]
        contours = Contour_AI.objects.filter(polygon__coveredby=image_date.polygon)
        for contour in contours:
            print(contour)
            polygon = GEOSGeometry(contour.polygon).geojson
            file_name = f'temporary_culture_{contour.id}'
            output_path_b04 = f"./media/B04_{file_name}.tiff"
            output_path_b8a = f"./media/B08a_{file_name}.tiff"
            output_path_b11 = f"./media/B11_{file_name}.tiff"

            input_path_b04 = f'./media/{image_date.B04}'
            input_path_b8a = f'./media/{image_date.B8A}'
            input_path_b11 = f'./media/{image_date.B11}'

            gdal.UseExceptions()
            cutting_error = []

            try:
                cutting_tiff(outputpath=output_path_b04, inputpath=input_path_b04, polygon=polygon)
            except Exception as b04_error:
                cutting_error.append(f'B04 layer cutting error {b04_error}, ')

            try:
                cutting_tiff(outputpath=output_path_b8a, inputpath=input_path_b8a, polygon=polygon)
            except Exception as b8a_error:
                cutting_error.append(f'B8A layer cutting error {b8a_error}, ')
            try:
                cutting_tiff(outputpath=output_path_b11, inputpath=input_path_b11, polygon=polygon)
            except Exception as b11_error:
                cutting_error.append(f'B11 layer cutting error {b11_error}')

            try:
                result = predict_from_raster_bands(red_path=output_path_b04, nir_path=output_path_b8a, swir_path=output_path_b11)
                if result == 0:
                    contour.culture = 'Пшеница'
                    contour.save()
                elif result == 1:
                    contour.culture = 'Картофель'
                    contour.save()
                elif result == 2:
                    contour.culture = 'Овёс'
                    contour.save()
                elif result == 3:
                    contour.culture = 'Лук'
                    contour.save()
                elif result == 4:
                    contour.culture = 'Кукуруза'
                    contour.save()
                elif result == 5:
                    contour.culture = 'Капуста'
                    contour.save()
                elif result == 6:
                    contour.culture = 'Гречиха'
                    contour.save()
                elif result == 7:
                    contour.culture = 'Подсолнечник'
                    contour.save()
                elif result == 8:
                    contour.culture = 'Хлопок'
                    contour.save()
                else:
                    contour.culture = 'Неизвестная культура'
                    contour.save()
            except Exception as e:
                print(e)
                pass

            # Search files with .tiff extension in current directory
            pattern = "./media/*.tiff"
            files = glob.glob(pattern)

        # deleting the files with tiff extension
        for file in files:
            os.remove(file)

        return Response('result', status=200)
