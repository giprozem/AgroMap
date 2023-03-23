from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import Region
from gip.serializers.region import RegionSerializer, RegionWithoutPolygonSerializer


class RegionAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='polygon',
                in_=openapi.IN_QUERY,
                description='Flag to include/exclude polygon data',
                type=openapi.TYPE_BOOLEAN,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='List of regions',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='Region ID'
                            ),
                            'name': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Region name'
                            ),
                            'polygon': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                description='Region polygon data',
                                properties={
                                    'type': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Polygon type'
                                    ),
                                    'coordinates': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        description='List of coordinates',
                                        items=openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_NUMBER
                                            )
                                        )
                                    )
                                }
                            )
                        }
                    )
                )
            ),
            400: openapi.Response(
                description='Bad request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Error message'
                        )
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        polygon = request.query_params.get('polygon')
        id = request.query_params.get('id')
        if polygon and id:
            query = Region.objects.all().filter(id__in=[int(id) for id in id.split(',')])
            serializer = RegionSerializer(query, many=True)
            return Response(serializer.data, status=200)
        elif id:
            query = Region.objects.all().filter(id__in=[int(id) for id in id.split(',')])
            serializer = RegionWithoutPolygonSerializer(query, many=True)
            return Response(serializer.data, status=200)
