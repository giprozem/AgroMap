from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import Region
from gip.serializers.region import RegionSerializer, RegionWithoutPolygonSerializer
from gip.schemas.region import get_region_schema


class RegionAPIView(APIView):
    @get_region_schema()
    def get(self, request, *args, **kwargs):
        polygon = request.query_params.get('polygon')
        if polygon:
            query = Region.objects.all()
            serializer = RegionSerializer(query, many=True)
            return Response(serializer.data, status=200)
        else:
            query = Region.objects.all()
            serializer = RegionWithoutPolygonSerializer(query, many=True)
            return Response(serializer.data, status=200)
