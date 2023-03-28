from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ai.productivity_funcs.training import initialize, predict, model_path
from gip.models.contour import Contour
from indexes.serializers.statistics_veg_index import ContourStatisticsSerializer


class PredictAIContourProductivity(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front'
    )
    def post(self, request, *args, **kwargs):
        contour = self.request.query_params['contour_id']
        response = Contour.objects.get(id=contour)
        serializer = ContourStatisticsSerializer(response)
        print(serializer.data)

        if response:
            return_list = serializer.data
            json_data = JSONRenderer().render(return_list)
            json_string = json_data.decode('utf-8')
            predict(model_path, json_string)
            return Response(serializer.data, status=200)
        return Response([], status=204)


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
