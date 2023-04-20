from drf_yasg import openapi
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
        """
               Retrieve contours statistics filtered by start and end dates.
               collect DS
        """
        start = request.query_params['start']
        end = request.query_params['end']
        queryset = Contour.objects.all().filter(
            is_deleted=False
        ).filter(
            productivity__isnull=False).filter(
            actual_veg_index__date__range=(
                start, end
            )
        )
        serializer_class = ContourStatisticsSerializer(queryset, many=True)
        return Response(serializer_class.data, status=200)


class ContourProductivityPredictAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front'
    )
    def post(self, request, *args, **kwargs):
        contour = self.request.query_params['contour_id']
        query = Contour.objects.get(id=contour)
        serializer = ContourStatisticsSerializer(query)
        return Response(serializer.data, status=200)
    