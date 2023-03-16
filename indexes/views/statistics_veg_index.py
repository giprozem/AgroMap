# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from gip.models import ContourYear
# from indexes.serializers.statistics_veg_index import ContourYearStatisticsSerializer
# from drf_yasg.utils import swagger_auto_schema
#
#
# class ContourYearAPIView(APIView):
#
#     @swagger_auto_schema(
#         operation_summary='do not required for front'
#     )
#     def get(self, request, *args, **kwargs):
#         queryset = ContourYear.objects.all()
#         serializer_class = ContourYearStatisticsSerializer(queryset, many=True)
#         return Response(serializer_class.data, status=200)
