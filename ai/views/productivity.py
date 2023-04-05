from threading import Thread

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.models import Contour_AI
from ai.utils.productivity import creating_veg_indexes
from ai.utils.productivity import creating_veg_indexes_image
from indexes.models import PredictedContourVegIndex
from ai.productivity_funcs.predicting import productivity_predict


class CreatingIndexAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front',
        operation_description='creating veg indexes'
    )
    def post(self, request, *args, **kwargs):
        thread_obj = Thread(target=creating_veg_indexes)
        thread_obj.start()
        return Response('finish', status=200)


class CreatingIndexSatellite(APIView):

    @swagger_auto_schema(
        operation_summary='do not required for front',
        operation_description='creating veg indexes in required in given satellite image id'
    )
    def get(self, request, *args, **kwargs):

        tread_obj = Thread(target=creating_veg_indexes_image, args=(request.query_params['satellite_id'], ))
        tread_obj.start()
        return Response('finish', status=200)


class PredictingProductivityAPIVie(APIView):

    def get(self, request, *args, **kwargs):
        veg = PredictedContourVegIndex.objects.filter(index_id=1, date='2022-06-21')
        for i in veg:
            result = productivity_predict(float(i.average_value))
            if result <= 0:
                result = 0
            contour = Contour_AI.objects.get(id=i.contour.id)
            contour.productivity = round(result, 3)
            contour.save()
            print(i.contour.id)
        return Response('ok', status=200)
