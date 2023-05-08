from threading import Thread

from django.db import connection
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.utils.predicting_culture import predicting_culture


class CulturePredict(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front',
        operation_description='predicting culture in given satellite image id'
    )
    def get(self, request, *args, **kwargs):
        thread_obj = Thread(target=predicting_culture, args=(request.query_params['satellite_id'],))
        thread_obj.start()
        return Response('result', status=200)


class PivotTableCulture(APIView):
    def get(self, request):
        culture = request.GET.get('culture')
        if culture:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                SELECT dst.id, aic.culture_id, MAX(aic.elevation) as max_elevation, MIN(aic.elevation) as min_elevation, 
                MAX(CASE WHEN cmv.name = 'NDVI' THEN ipc.average_value END) as ndvi_max, MIN(CASE WHEN cmv.name = 'NDVI' THEN ipc.average_value END) as ndvi_min,
                MAX(CASE WHEN cmv.name = 'VARI' THEN ipc.average_value END) as vari_max, MIN(CASE WHEN cmv.name = 'VARI' THEN ipc.average_value END) as vari_min,
                MAX(CASE WHEN cmv.name = 'NDWI' THEN ipc.average_value END) as ndwi_max, MIN(CASE WHEN cmv.name = 'NDWI' THEN ipc.average_value END) as ndwi_min,
                MAX(CASE WHEN cmv.name = 'NDRE' THEN ipc.average_value END) as ndre_max, MIN(CASE WHEN cmv.name = 'NDRE' THEN ipc.average_value END) as ndre_min,
                MAX(CASE WHEN cmv.name = 'SAVI' THEN ipc.average_value END) as savi_max, MIN(CASE WHEN cmv.name = 'SAVI' THEN ipc.average_value END) as savi_min,
                dst.name
                FROM ai_contour_ai as aic
                LEFT JOIN gip_district as dst ON dst.id=aic.district_id
                LEFT JOIN indexes_predictedcontourvegindex as ipc ON aic.id=ipc.contour_id
                LEFT JOIN culture_model_vegetationindex as cmv ON cmv.id=ipc.index_id
                WHERE aic.culture_id = {culture}
                GROUP BY dst.id, aic.culture_id;
                """)
                rows = cursor.fetchall()
            data = []
            for i in rows:
                data.append(
                    {'district_id': i[0], 'culture_id': i[1], 'max_elevation': i[2], 'min_elevation': i[3],
                     'ndvi_max': i[4],
                     'ndvi_min': i[5], 'vari_max': i[6], 'vari_min': i[7], 'ndwi_max': i[8], 'ndwi_min': i[9],
                     'ndre_max': i[10],
                     'ndre_min': i[11], 'savi_max': i[12], 'savi_min': i[13], 'district_name': i[14], 'year': '2022'}
                )
            return Response(data)
        else:
            return Response(data={"message": "parameter 'culture' is required"}, status=400)
