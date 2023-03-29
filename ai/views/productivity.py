from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.productivity_funcs.training import initialize, predict, model_path
from ai.serializers.productivity import ContourAISerializer
from ai.utils.productivity import predicting_productivity
from gip.models.contour import Contour
from indexes.serializers.statistics_veg_index import ContourStatisticsSerializer
from ai.models.predicted_contour import Contour_AI
from threading import Thread
from ai.utils.productivity import creating_veg_indexes


class PredictAIContourProductivity(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front'
    )
    def post(self, request, *args, **kwargs):
        contour = self.request.query_params['contour_id']
        response = Contour.objects.get(id=contour)
        serializer = ContourStatisticsSerializer(response)
        res = [serializer.data]
        json_data = JSONRenderer().render(res)
        json_string = json_data.decode('utf-8')
        result = predict(model_path=model_path, predict_path=json_string)
        response.productivity = result
        response.save()
        return Response(result, status=200)


class DataToTrainProductivityAPIView(APIView):

    @swagger_auto_schema(
        operation_summary='do not required for front',
        operation_description='Training model of productivity'
    )
    def post(self, request, *args, **kwargs):
        response = Contour.objects.all()
        serializer = ContourStatisticsSerializer(response, many=True)
        if response:
            return_list = serializer.data
            json_data = JSONRenderer().render(return_list)
            json_string = json_data.decode('utf-8')
            initialize(json_string)
            return Response(serializer.data, status=200)
        return Response([], status=204)


class CheckAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front',
        operation_description='Productivity prediction'
    )
    def get(self, request, *args, **kwargs):
        for i in range(1, 5):
            try:
                predicting_productivity(i)
            except Exception as e:
                print(e)
                pass
        return Response('ok', status=200)


class CreatingIndexAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front',
        operation_description='creating veg indexes'
    )
    def post(self, request, *args, **kwargs):
        thread_obj = Thread(target=creating_veg_indexes)
        thread_obj.start()
        return Response('finish', status=200)

