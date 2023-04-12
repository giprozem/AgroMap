from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from gip.models import Conton
from gip.serializers.conton import ContonSerializer, ContonWithoutPolygonSerializer


class ContonAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page_size',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Page_size is required'
            ),
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
        conton = request.query_params.get('id')
        paginator = PageNumberPagination()
        paginator.page_size = request.query_params.get('page_size')
        if polygon:
            if district and conton:
                query = Conton.objects.filter(district_id__in=[int(district_id) for district_id in district.split(',')],
                                                id__in=[int(pk) for pk in conton.split(',')])
            elif district:
                query = Conton.objects.filter(district_id__in=[int(district_id) for district_id in district.split(',')])
            elif conton:
                query = Conton.objects.all().filter(id__in=[int(pk) for pk in conton.split(',')])
            else:
                query = Conton.objects.all()
            result = paginator.paginate_queryset(query, request)
            serializer = ContonSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            if district and conton:
                query = Conton.objects.filter(district_id__in=[int(district_id) for district_id in district.split(',')],
                                                id__in=[int(pk) for pk in conton.split(',')])
            elif district:
                query = Conton.objects.filter(district_id__in=[int(district_id) for district_id in district.split(',')])
            elif conton:
                query = Conton.objects.all().filter(id__in=[int(pk) for pk in conton.split(',')])
            else:
                query = Conton.objects.all()
            result = paginator.paginate_queryset(query, request)
            serializer = ContonWithoutPolygonSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
