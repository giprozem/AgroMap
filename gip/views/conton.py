from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import Conton
from gip.serializers.conton import ContonSerializer, ContonWithoutPolygonSerializer


class ContonAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'polygon',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='If set, returns the serialized polygon for each district. '
                            'If doesnot set, returns only the district data without polygons.'
            ),
            openapi.Parameter(
                'district_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='If `polygon` is set, this parameter can be used to filter districts by district ID.'
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
                            'district_id': openapi.Schema(type=openapi.TYPE_INTEGER),
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
        polygon = request.query_params.get('polygon')
        district = request.query_params.get('district_id')
        id = request.query_params.get('id')
        if polygon and id:
            query = Conton.objects.all().filter(id__in=[int(id) for id in id.split(',')])
            serializer = ContonSerializer(query, many=True)
            return Response(serializer.data, status=200)
        elif id and polygon and district:
            query = Conton.objects.filter(district_id__in=[int(district_id) for district_id in district.split(',')],
                                          id__in=[int(id) for id in id.split(',')])
            serializer = ContonSerializer(query, many=True)
            return Response(serializer.data, status=200)
        elif id:
            query = Conton.objects.all().filter(id__in=[int(id) for id in id.split(',')])
            serializer = ContonWithoutPolygonSerializer(query, many=True)
            return Response(serializer.data, status=200)
        elif id and district:
            query = Conton.objects.filter(district__in=[int(district_id) for district_id in district.split(',')],
                                          id__in=[int(id) for id in id.split(',')])
            serializer = ContonWithoutPolygonSerializer(query, many=True)
            return Response(serializer.data, status=200)
