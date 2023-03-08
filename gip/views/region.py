from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import Region
from gip.serializers.region import RegionSerializer


class RegionAPIView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=RegionSerializer(many=True)
            ),
            400: openapi.Response(
                description='We have no data to show',
                schema=RegionSerializer(many=True)
            )
        },
        operation_summary='return all regions with all data'
    )
    def get(self, request, *args, **kwargs):
        queryset = Region.objects.all()
        serializer = RegionSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
