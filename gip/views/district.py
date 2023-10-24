from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from gip.models import District
from gip.serializers.district import DistrictSerializer, DistrictWithoutPolygonSerializer
from gip.schemas.district import get_district_schema


class DistrictAPIView(APIView):

    @get_district_schema()
    def get(self, request, *args, **kwargs):
        polygon = request.query_params.get('polygon')
        region = request.query_params.get('region_id')
        district = request.query_params.get('id')
        if polygon:
            if region and district:
                query = District.objects.filter(region_id__in=[int(region_id) for region_id in region.split(',')],
                                                id__in=[int(pk) for pk in district.split(',')]).order_by('id')
            elif region:
                query = District.objects.filter(
                    region_id__in=[int(region_id) for region_id in region.split(',')]).order_by('id')
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
                query = District.objects.filter(
                    region_id__in=[int(region_id) for region_id in region.split(',')]).order_by('id')
            elif district:
                query = District.objects.all().filter(id__in=[int(pk) for pk in district.split(',')]).order_by('id')
            else:
                query = District.objects.all().order_by('id')
            paginator = PageNumberPagination()
            paginator.page_size = request.query_params.get('page_size', 20)
            result = paginator.paginate_queryset(query, request)
            serializer = DistrictWithoutPolygonSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)
