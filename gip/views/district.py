from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from gip.models import District
from gip.serializers.district import DistrictSerializer, DistrictWithoutPolygonSerializer


class DistrictAPIView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page_size',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Page_size is optional'
            ),
            openapi.Parameter(
                'polygon',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description='If set, returns the serialized polygon for each district. '
                            'If doesnot set, returns only the district data without polygons.'
            ),
            openapi.Parameter(
                'region_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='If `polygon` is set, this parameter can be used to filter districts by region ID.'
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
        polygon = request.query_params.get('polygon')
        region = request.query_params.get('region_id')
        district = request.query_params.get('id')
        if polygon:
            if region and district:
                query = District.objects.filter(region_id__in=[int(region_id) for region_id in region.split(',')],
                                                id__in=[int(pk) for pk in district.split(',')]).order_by('id')
            elif region:
                query = District.objects.filter(region_id__in=[int(region_id) for region_id in region.split(',')]).order_by('id')
            elif district:
                query = District.objects.all().filter(id__in=[int(pk) for pk in district.split(',')]).order_by('id')
            else:
                query = District.objects.all().order_by('id')
            serializer = DistrictSerializer(query, many=True)
            return Response(serializer.data, status=200)
        else:
            if region and district:
                query = District.objects.filter(region_id__in=[int(region_id) for region_id in region.split(',')],
                                                id__in=[int(pk) for pk in district.split(',')]).order_by('id')
            elif region:
                query = District.objects.filter(region_id__in=[int(region_id) for region_id in region.split(',')]).order_by('id')
            elif district:
                query = District.objects.all().filter(id__in=[int(pk) for pk in district.split(',')]).order_by('id')
            else:
                query = District.objects.all().order_by('id')
            paginator = PageNumberPagination()
            paginator.page_size = request.query_params.get('page_size', 20)
            result = paginator.paginate_queryset(query, request)
            serializer = DistrictWithoutPolygonSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
