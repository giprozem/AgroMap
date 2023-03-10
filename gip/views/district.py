from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import District
from gip.serializers.district import DistrictSerializer, DistrictWithoutPolygonSerializer


class DistrictAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'polygon',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='If set to `true`, returns the serialized polygon for each district. '
                            'If set to `false`, returns only the district data without polygons.'
            ),
            openapi.Parameter(
                'region_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='If `polygon` is set to `false`, this parameter can be used to filter districts by region ID.'
            ),
        ],
        responses={
            200: openapi.Response(
                'OK',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'name': openapi.Schema(type=openapi.TYPE_STRING),
                            'region_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'polygon': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, example='Polygon'),
                                    'coordinates': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(type=openapi.TYPE_NUMBER)
                                            )
                                        )
                                    )
                                }
                            )
                        }
                    )
                )
            ),
            400: openapi.Response('Bad Request')
        }
    )
    def get(self, request, *args, **kwargs):
        print(request.query_params)
        if request.query_params['polygon'] == 'true':
            query = District.objects.all()
            serializer = DistrictSerializer(query, many=True)
            return Response(serializer.data, status=200)
        elif request.query_params['polygon'] == 'false':
            query = District.objects.all()
            serializer = DistrictWithoutPolygonSerializer(query, many=True)
            return Response(serializer.data, status=200)
        elif request.query_params['polygon'] == 'false' and request.query_params['region_id']:
            query = District.objects.filter(region_id=request.query_params['region_id'])
            serializer = DistrictWithoutPolygonSerializer(query, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response('Required polygon param', status=400)
