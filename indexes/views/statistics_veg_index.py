from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import Contour
from indexes.serializers.statistics_veg_index import ContourStatisticsSerializer
from drf_yasg.utils import swagger_auto_schema


class ContourAPIView(APIView):

    @swagger_auto_schema(
        operation_summary='do not required for front'
    )
    def get(self, request, *args, **kwargs):
        queryset = Contour.objects.all()
        serializer_class = ContourStatisticsSerializer(queryset, many=True)
        return Response(serializer_class.data, status=200)


class ContourProductivityPredictAPIView(APIView):

    def post(self, request, *args, **kwargs):
        contour = self.request.query_params['contour_id']
        query = Contour.objects.get(id=contour)
        serializer = ContourStatisticsSerializer(query, many=True)
        return Response(serializer.data, status=200)
    