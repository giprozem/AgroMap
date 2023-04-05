from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from gip.models.contour import Contour
from gip.pagination.contour_pagination import SearchContourPagination
from gip.serializers.contour import ContourSerializer, AuthDetailContourSerializer, UpdateAuthDetailContourSerializer


class AuthDetailContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all().order_by('id').filter(is_deleted=False)
    serializer_class = AuthDetailContourSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UpdateAuthDetailContourSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response('Contour is deleted')


class SearchContourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ink', 'conton']
    pagination_class = SearchContourPagination


class ContourSearchAPIView(ListAPIView):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
    pagination_class = SearchContourPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['ink']


class FilterContourAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER),
            openapi.Parameter('land_type', openapi.IN_QUERY, description="Land type", type=openapi.TYPE_INTEGER),
            openapi.Parameter('region', openapi.IN_QUERY, description="Region", type=openapi.TYPE_INTEGER),
            openapi.Parameter('district', openapi.IN_QUERY, description="District", type=openapi.TYPE_INTEGER),
            openapi.Parameter('conton', openapi.IN_QUERY, description="Conton", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                    'features': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'type': openapi.Schema(type=openapi.TYPE_STRING),
                                'properties': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'contour_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'contour_ink': openapi.Schema(type=openapi.TYPE_STRING),
                                        'conton_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'farmer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'contour_year_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'productivity': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'land_type': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    }
                                ),
                                'geometry': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'type': openapi.Schema(type=openapi.TYPE_STRING),
                                        'coordinates': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_ARRAY,
                                                    items=openapi.Schema(
                                                        type=openapi.TYPE_NUMBER,
                                                    ),
                                                ),
                                            ),
                                        ),
                                    },
                                ),
                            },
                        ),
                    ),
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        year = request.GET.get('year')
        land_type = request.GET.get('land_type')
        district = request.GET.get('district')
        conton = request.GET.get('conton')
        ai = request.GET.get('ai')
        if region and district and conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               SELECT cntr.id AS contour_id, 
                               cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                               cntr.year, cntr.area_ha, cntr.productivity,
                               rgn.name_ru, rgn.name_ky, rgn.name_en,
                               dst.name_ru, dst.name_ky, dst.name_en,
                               cntn.name_ru, cntn.name_ky, cntn.name_en,
                               land.name_ru, land.name_ky, land.name_en,
                               cntr.is_deleted,
                               St_AsGeoJSON(cntr.polygon) as polygon   
                               FROM gip_contour AS cntr 
                               JOIN gip_landtype AS land ON land.id=cntr.type_id
                               JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                               JOIN gip_district AS dst ON dst.id=cntn.district_id
                               JOIN gip_region AS rgn ON rgn.id=dst.region_id
                               where rgn.id in ({region}) and dst.id in ({district}) and cntn.id in ({conton}) 
                               and cntr.type_id in ({land_type}) and cntr.year='{year}' 
                               and cntr.is_deleted=false order by cntr.id;
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[3],
                                                                      'land_type_id': i[1],
                                                                      'year': i[4], 'ink': i[2],
                                                                      'productivity': i[6], 'area_ha': i[5],
                                                                      'region_ru': i[7], 'region_ky': i[8],
                                                                      'region_en': i[9],
                                                                      'district_ru': i[10], 'district_ky': i[11],
                                                                      'district_en': i[12],
                                                                      'conton_ru': i[13], 'conton_ky': i[14],
                                                                      'conton_en': i[15],
                                                                      'land_type_ru': i[16], 'land_type_ky': i[17],
                                                                      'land_type_en': i[18]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif region and district and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, 
                                cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                cntr.year, cntr.area_ha, cntr.productivity,
                                rgn.name_ru, rgn.name_ky, rgn.name_en,
                                dst.name_ru, dst.name_ky, dst.name_en,
                                cntn.name_ru, cntn.name_ky, cntn.name_en,
                                land.name_ru, land.name_ky, land.name_en,
                                cntr.is_deleted,
                                St_AsGeoJSON(cntr.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                JOIN gip_landtype AS land ON land.id=cntr.type_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where cntr.type_id in ({land_type}) and rgn.id in ({region}) and cntr.year='{year}'
                                and dst.id in ({district}) and cntr.is_deleted=false order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[3],
                                                                      'land_type_id': i[1],
                                                                      'year': i[4], 'ink': i[2],
                                                                      'productivity': i[6], 'area_ha': i[5],
                                                                      'region_ru': i[7], 'region_ky': i[8],
                                                                      'region_en': i[9],
                                                                      'district_ru': i[10], 'district_ky': i[11],
                                                                      'district_en': i[12],
                                                                      'conton_ru': i[13], 'conton_ky': i[14],
                                                                      'conton_en': i[15],
                                                                      'land_type_ru': i[16], 'land_type_ky': i[17],
                                                                      'land_type_en': i[18]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif ai and region and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, cntr.type_id AS land_type_id, cntr.year, 
                                cntr.area_ha, cntr.productivity, cntr.district_id, cntr.conton_id, land.name, cntr.is_deleted,
                                rgn.id, St_AsGeoJSON(cntr.polygon) as polygon   
                                FROM ai_contour_ai AS cntr
                                JOIN gip_landtype AS land ON land.id=cntr.type_id
                                JOIN gip_district AS dst ON dst.id=cntr.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                WHERE rgn.id in ({region}) 
                                and cntr.type_id in ({land_type}) and cntr.year='{year}' and cntr.id > 11016
                                and cntr.is_deleted=false order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'land_type_id': i[1],
                                                                      'year': i[2], 'area_ha': i[3],
                                                                      'productivity': i[4],
                                                                      'district': i[5],
                                                                      'conton': i[6],
                                                                      'land_type': i[7], 'region': i[9]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif region and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id,
                                cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                cntr.year, cntr.area_ha, cntr.productivity,
                                rgn.name_ru, rgn.name_ky, rgn.name_en,
                                dst.name_ru, dst.name_ky, dst.name_en,
                                cntn.name_ru, cntn.name_ky, cntn.name_en,
                                land.name_ru, land.name_ky, land.name_en,
                                cntr.is_deleted,
                                St_AsGeoJSON(cntr.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                JOIN gip_landtype AS land ON land.id=cntr.type_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where cntr.type_id in ({land_type}) and rgn.id in ({region}) and cntr.year='{year}'
                                and cntr.is_deleted=false order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[3],
                                                                      'land_type_id': i[1],
                                                                      'year': i[4], 'ink': i[2],
                                                                      'productivity': i[6], 'area_ha': i[5],
                                                                      'region_ru': i[7], 'region_ky': i[8],
                                                                      'region_en': i[9],
                                                                      'district_ru': i[10], 'district_ky': i[11],
                                                                      'district_en': i[12],
                                                                      'conton_ru': i[13], 'conton_ky': i[14],
                                                                      'conton_en': i[15],
                                                                      'land_type_ru': i[16], 'land_type_ky': i[17],
                                                                      'land_type_en': i[18]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif ai and district and conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, cntr.type_id AS land_type_id, cntr.year, 
                                cntr.area_ha, cntr.productivity, cntr.district_id, cntr.conton_id, land.name, cntr.is_deleted,  
                                St_AsGeoJSON(cntr.polygon) as polygon   
                                FROM ai_contour_ai AS cntr 
                                JOIN gip_landtype AS land ON land.id=cntr.type_id
                                WHERE cntr.district_id in ({district}) and cntr.conton_id in ({conton}) 
                                and cntr.type_id in ({land_type}) and cntr.year='{year}' and cntr.id > 11016
                                and cntr.is_deleted=false order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'land_type_id': i[1],
                                                                      'year': i[2], 'area_ha': i[3],
                                                                      'productivity': i[4],
                                                                      'district': i[5],
                                                                      'conton': i[6],
                                                                      'land_type': i[7]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif district and conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                    SELECT cntr.id AS contour_id,
                                    cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                    cntr.year, cntr.area_ha, cntr.productivity,
                                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                                    dst.name_ru, dst.name_ky, dst.name_en,
                                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                                    land.name_ru, land.name_ky, land.name_en,
                                    cntr.is_deleted,
                                    St_AsGeoJSON(cntr.polygon) as polygon  
                                    FROM gip_contour AS cntr 
                                    JOIN gip_landtype AS land ON land.id=cntr.type_id
                                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                    where cntr.type_id in ({land_type}) and dst.id in ({district}) and cntr.year='{year}'
                                    and cntn.id in ({conton}) and cntr.is_deleted=false order by cntr.id;
                                    """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[3],
                                                                      'land_type_id': i[1],
                                                                      'year': i[4], 'ink': i[2],
                                                                      'productivity': i[6], 'area_ha': i[5],
                                                                      'region_ru': i[7], 'region_ky': i[8],
                                                                      'region_en': i[9],
                                                                      'district_ru': i[10], 'district_ky': i[11],
                                                                      'district_en': i[12],
                                                                      'conton_ru': i[13], 'conton_ky': i[14],
                                                                      'conton_en': i[15],
                                                                      'land_type_ru': i[16], 'land_type_ky': i[17],
                                                                      'land_type_en': i[18]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif ai and district and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, cntr.type_id AS land_type_id, cntr.year, 
                                cntr.area_ha, cntr.productivity, cntr.district_id, cntr.conton_id, land.name, cntr.is_deleted,  
                                St_AsGeoJSON(cntr.polygon) as polygon   
                                FROM ai_contour_ai AS cntr 
                                JOIN gip_landtype AS land ON land.id=cntr.type_id
                                WHERE cntr.district_id in ({district}) and cntr.type_id in ({land_type}) 
                                and cntr.year='{year}' and cntr.id > 11016 and cntr.is_deleted=false order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'land_type_id': i[1],
                                                                      'year': i[2], 'area_ha': i[3],
                                                                      'productivity': i[4],
                                                                      'district': i[5],
                                                                      'conton': i[6],
                                                                      'land_type': i[7]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif district and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id,
                                cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                cntr.year, cntr.area_ha, cntr.productivity,
                                rgn.name_ru, rgn.name_ky, rgn.name_en,
                                dst.name_ru, dst.name_ky, dst.name_en,
                                cntn.name_ru, cntn.name_ky, cntn.name_en,
                                land.name_ru, land.name_ky, land.name_en,
                                cntr.is_deleted,
                                St_AsGeoJSON(cntr.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                JOIN gip_landtype AS land ON land.id=cntr.type_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where cntr.type_id in ({land_type}) and cntr.year='{year}' and dst.id in ({district})
                                and cntr.is_deleted=false order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[3],
                                                                      'land_type_id': i[1],
                                                                      'year': i[4], 'ink': i[2],
                                                                      'productivity': i[6], 'area_ha': i[5],
                                                                      'region_ru': i[7], 'region_ky': i[8],
                                                                      'region_en': i[9],
                                                                      'district_ru': i[10], 'district_ky': i[11],
                                                                      'district_en': i[12],
                                                                      'conton_ru': i[13], 'conton_ky': i[14],
                                                                      'conton_en': i[15],
                                                                      'land_type_ru': i[16], 'land_type_ky': i[17],
                                                                      'land_type_en': i[18]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif ai and conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, cntr.type_id AS land_type_id, cntr.year, 
                                cntr.area_ha, cntr.productivity, cntr.district_id, cntr.conton_id, land.name, cntr.is_deleted,  
                                St_AsGeoJSON(cntr.polygon) as polygon   
                                FROM ai_contour_ai AS cntr 
                                JOIN gip_landtype AS land ON land.id=cntr.type_id
                                WHERE cntr.conton_id in ({conton}) AND cntr.type_id in ({land_type}) AND cntr.year='{year}' 
                                AND cntr.is_deleted=false and cntr.id > 11016 ORDER BY cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'land_type_id': i[1],
                                                                      'year': i[2], 'area_ha': i[3],
                                                                      'productivity': i[4],
                                                                      'district': i[5],
                                                                      'conton': i[6],
                                                                      'land_type': i[7]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               SELECT cntr.id AS contour_id,
                               cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                               cntr.year, cntr.area_ha, cntr.productivity,
                               rgn.name_ru, rgn.name_ky, rgn.name_en,
                               dst.name_ru, dst.name_ky, dst.name_en,
                               cntn.name_ru, cntn.name_ky, cntn.name_en,
                               land.name_ru, land.name_ky, land.name_en,
                               cntr.is_deleted,
                               St_AsGeoJSON(cntr.polygon) as polygon    
                               FROM gip_contour AS cntr 
                               JOIN gip_landtype AS land ON land.id=cntr.type_id
                               JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                               JOIN gip_district AS dst ON dst.id=cntn.district_id
                               JOIN gip_region AS rgn ON rgn.id=dst.region_id
                               where cntn.id in ({conton}) and cntr.type_id in ({land_type}) and cntr.year='{year}'
                               and cntr.is_deleted=false order by cntr.id;
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[3],
                                                                      'land_type_id': i[1],
                                                                      'year': i[4], 'ink': i[2],
                                                                      'productivity': i[6], 'area_ha': i[5],
                                                                      'region_ru': i[7], 'region_ky': i[8],
                                                                      'region_en': i[9],
                                                                      'district_ru': i[10], 'district_ky': i[11],
                                                                      'district_en': i[12],
                                                                      'conton_ru': i[13], 'conton_ky': i[14],
                                                                      'conton_en': i[15],
                                                                      'land_type_ru': i[16], 'land_type_ky': i[17],
                                                                      'land_type_en': i[18]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif ai and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, cntr.type_id AS land_type_id, cntr.year, 
                                cntr.area_ha, cntr.productivity, cntr.district_id, cntr.conton_id, land.name, cntr.is_deleted,  
                                St_AsGeoJSON(cntr.polygon) as polygon   
                                FROM ai_contour_ai AS cntr 
                                JOIN gip_landtype AS land ON land.id=cntr.type_id
                                WHERE cntr.type_id in ({land_type}) and cntr.year='{year}' 
                                and cntr.is_deleted=false and cntr.id > 11016 order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'land_type_id': i[1],
                                                                      'year': i[2], 'area_ha': i[3],
                                                                      'productivity': i[4],
                                                                      'district': i[5],
                                                                      'conton': i[6],
                                                                      'land_type': i[7]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id,
                                cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                cntr.year, cntr.area_ha, cntr.productivity,
                                rgn.name_ru, rgn.name_ky, rgn.name_en,
                                dst.name_ru, dst.name_ky, dst.name_en,
                                cntn.name_ru, cntn.name_ky, cntn.name_en,
                                land.name_ru, land.name_ky, land.name_en,
                                cntr.is_deleted,
                                St_AsGeoJSON(cntr.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                JOIN gip_landtype AS land ON land.id=cntr.type_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where cntr.year='{year}' and cntr.type_id in ({land_type})
                                and cntr.is_deleted=false order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[3],
                                                                      'land_type_id': i[1],
                                                                      'year': i[4], 'ink': i[2],
                                                                      'productivity': i[6], 'area_ha': i[5],
                                                                      'region_ru': i[7], 'region_ky': i[8],
                                                                      'region_en': i[9],
                                                                      'district_ru': i[10], 'district_ky': i[11],
                                                                      'district_en': i[12],
                                                                      'conton_ru': i[13], 'conton_ky': i[14],
                                                                      'conton_en': i[15],
                                                                      'land_type_ru': i[16], 'land_type_ky': i[17],
                                                                      'land_type_en': i[18]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        else:
            return Response(data={"message": "parameter 'year or land_type' is required"}, status=400)


class ContourStatisticsAPIView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        culture = request.GET.get('culture')
        if region and culture:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                select culture_name, count(contour_id) as cntr_id_count, sum(area_ha) as total_area_ha, region_name, 
                round(sum(area_ha * coefficient_crop)::numeric, 2) as cropy_yeld
                from (
                  select cntr.id as contour_id, cl.name as culture_name, 
                  rank() over (PARTITION BY cntr.id ORDER BY cy.year DESC) AS culture_rank, area_ha, 
                  rgn.name as region_name, cl.coefficient_crop as coefficient_crop
                  from gip_contour as cntr
                  join gip_conton as cntn 
                  on cntn.id=cntr.conton_id 
                  join gip_district as dst 
                  on dst.id=cntn.district_id 
                  join gip_region as rgn 
                  on rgn.id=dst.region_id
                  join gip_landtype as ltp
                  on ltp.id=cntr.type_id 
                  left join gip_cropyield as cy
                  on cy.contour_id = cntr.id
                  left join gip_culture as cl
                  on cy.culture_id = cl.id
                  where rgn.id in ({region}) and cntr.type_id=1 and (cl.id in ({culture}))) as temp
                        where culture_rank=1
                        group by culture_name, region_name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"properties": {'culture': i[0], 'count_contour': i[1],
                                                "crop_yield": i[-1], 'area_ha': i[2], 'region': i[-2]}})
                return Response(data)
        elif region:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                select culture_name, count(contour_id) as cntr_id_count, sum(area_ha) as total_area_ha, region_name,
                round(sum(area_ha * coefficient_crop)::numeric, 2) as cropy_yeld 
                from (
                  select cntr.id as contour_id, cl.name as culture_name, 
                  rank() over (PARTITION BY cntr.id ORDER BY cy.year DESC) AS culture_rank, area_ha, 
                  rgn.name as region_name, cl.coefficient_crop as coefficient_crop
                  from gip_contour as cntr
                  join gip_conton as cntn 
                  on cntn.id=cntr.conton_id 
                  join gip_district as dst 
                  on dst.id=cntn.district_id 
                  join gip_region as rgn 
                  on rgn.id=dst.region_id
                  join gip_landtype as ltp
                  on ltp.id=cntr.type_id 
                  left join gip_cropyield as cy
                  on cy.contour_id = cntr.id
                  left join gip_culture as cl
                  on cy.culture_id = cl.id
                  where rgn.id in ({region}) and cntr.type_id=1) as temp
                        where culture_rank=1
                        group by culture_name, region_name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"properties": {'culture': i[0], 'count_contour': i[1],
                                                "crop_yield": i[-1], 'area_ha': i[2], 'region': i[-2]}})
                return Response(data)
        else:
            return Response(data={"message": "parameter 'region or culture' is required"}, status=400)


class StatisticsContourProductivityAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER),
            openapi.Parameter('land_type', openapi.IN_QUERY, description="Land type", type=openapi.TYPE_INTEGER),
            openapi.Parameter('region', openapi.IN_QUERY, description="Region", type=openapi.TYPE_INTEGER),
            openapi.Parameter('district', openapi.IN_QUERY, description="District", type=openapi.TYPE_INTEGER),
            openapi.Parameter('conton', openapi.IN_QUERY, description="Conton", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                    'features': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'type': openapi.Schema(type=openapi.TYPE_STRING),
                                'properties': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'contour_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'contour_ink': openapi.Schema(type=openapi.TYPE_STRING),
                                        'conton_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'farmer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'contour_year_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'productivity': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'land_type': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    }
                                ),
                                'geometry': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'type': openapi.Schema(type=openapi.TYPE_STRING),
                                        'coordinates': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_ARRAY,
                                                    items=openapi.Schema(
                                                        type=openapi.TYPE_NUMBER,
                                                    ),
                                                ),
                                            ),
                                        ),
                                    },
                                ),
                            },
                        ),
                    ),
                },
            ),
        },

    )
    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        year = request.GET.get('year')
        land_type = request.GET.get('land_type')
        district = request.GET.get('district')
        conton = request.GET.get('conton')
        if region and district and conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end)) as "Productive",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "productive_pct",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end) / sum(cntr .area_ha) * 100) as "unproductive_pct",
                    cntr.is_deleted, cntn.name
                    FROM gip_contour AS cntr 
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where cntr.year='{year}' and cntr.type_id in ({land_type}) and cntn.id in ({conton}) 
                    and rgn.id in ({region}) and dst.id in ({district})
                    and cntr.is_deleted=false
                    group by cntn.name, cntr.is_deleted;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'name': i[-1], 'type': 'Conton', 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif region and district and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end)) as "Productive",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "productive_pct",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "unproductive_pct",
                    cntr.is_deleted, cntn.name
                    FROM gip_contour AS cntr 
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where rgn.id in ({region}) and cntr.type_id in ({land_type}) and cntr.year='{year}' and dst.id in ({district})
                    and cntr.is_deleted=false group by cntn.name, cntr.is_deleted;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'name': i[-1], 'type': 'Conton', 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif region and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end)) as "Productive",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "productive_pct",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "unproductive_pct",
                    cntr.is_deleted, rgn.name, dst.name
                    FROM gip_contour AS cntr 
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where rgn.id in ({region}) and cntr.type_id in ({land_type}) and cntr.year='{year}'
                    and cntr.is_deleted=false group by rgn.name, dst.name, cntr.is_deleted;""")
                rows = cursor.fetchall()
                total = sum([row[0] for row in rows]) + sum([row[1] for row in rows])
                data = []
                for i in rows:
                    data.append({'name': i[-1], 'type': 'District', 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response({
                    "name": rows[0][5],
                    "type": "Region",
                    'Productive': {'ha': sum([row[0] for row in rows]),
                                   'percent': round(sum([row[0] for row in rows]) / total * 100)},
                    "Unproductive": {
                        "ha": sum([row[1] for row in rows]),
                        "percent": round(sum([row[1] for row in rows]) / total * 100)
                    },
                    "Districts": data
                })
        elif district and conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end)) as "Productive",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "productive_pct",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "unproductive_pct",
                    cntr.is_deleted, cntn.name
                    FROM gip_contour AS cntr 
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    where cntr.year='{year}' and cntr.type_id in ({land_type}) and dst.id in ({district})
                    and cntn.id in ({conton}) and cntr.is_deleted=false group by cntn.name, cntr.is_deleted;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'name': i[-1], 'type': 'Conton', 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif district and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end)) as "Productive",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "productive_pct",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "unproductive_pct",
                    cntr.is_deleted, dst.name, cntn.name
                    FROM gip_contour AS cntr 
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where cntr.year='2022' and cntr.type_id in (2) and dst.id in (8)
                    and cntr.is_deleted=false group by dst.name, cntn.name, cntr.is_deleted;""")
                rows = cursor.fetchall()
                total = sum([row[0] for row in rows]) + sum([row[1] for row in rows])
                data = []
                for i in rows:
                    data.append({'name': i[-1], 'type': 'Conton', 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response({
                    "name": rows[0][5],
                    "type": "District",
                    'Productive': {'ha': sum([row[0] for row in rows]),
                                   'percent': round(sum([row[0] for row in rows]) / total * 100)},
                    "Unproductive": {
                        "ha": sum([row[1] for row in rows]),
                        "percent": round(sum([row[1] for row in rows]) / total * 100)
                    },
                    "Contons": data
                })
        elif conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end)) as "Productive",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "productive_pct",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "unproductive_pct",
                    cntr.is_deleted, cntn.name 
                    FROM gip_contour AS cntr 
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where cntr.year='{year}' and cntr.type_id in ({land_type}) and cntn.id in ({conton})
                    and cntr.is_deleted=false group by cntn.name, cntr.is_deleted;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'name': i[-1], 'type': 'Conton', 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end)) as "Productive",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "productive_pct",
                    round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "unproductive_pct",
                    cntr.is_deleted, rgn.name 
                    FROM gip_contour AS cntr  
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where cntr.year='{year}' and cntr.type_id in ({land_type})
                    and cntr.is_deleted=false group by rgn.name, cntr.is_deleted;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'name': i[-1], 'type': 'Region', 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        else:
            return Response(data={"message": "parameter 'year and land_type' is required"}, status=400)


class MapContourProductivityAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER),
            openapi.Parameter('land_type', openapi.IN_QUERY, description="Land type", type=openapi.TYPE_INTEGER),
            openapi.Parameter('region', openapi.IN_QUERY, description="Region", type=openapi.TYPE_INTEGER),
            openapi.Parameter('district', openapi.IN_QUERY, description="District", type=openapi.TYPE_INTEGER),
            openapi.Parameter('conton', openapi.IN_QUERY, description="Conton", type=openapi.TYPE_INTEGER),
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                    'features': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'type': openapi.Schema(type=openapi.TYPE_STRING),
                                'properties': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'contour_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'contour_ink': openapi.Schema(type=openapi.TYPE_STRING),
                                        'conton_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'farmer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'contour_year_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'productivity': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'land_type': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    }
                                ),
                                'geometry': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'type': openapi.Schema(type=openapi.TYPE_STRING),
                                        'coordinates': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(
                                                    type=openapi.TYPE_ARRAY,
                                                    items=openapi.Schema(
                                                        type=openapi.TYPE_NUMBER,
                                                    ),
                                                ),
                                            ),
                                        ),
                                    },
                                ),
                            },
                        ),
                    ),
                },
            ),
        },

    )
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        year = request.GET.get('year')
        land_type = request.GET.get('land_type')
        district = request.GET.get('district')
        conton = request.GET.get('conton')
        if region and district and conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (cntr.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id,
                    cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    cntr.year, cntr.area_ha, cntr.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    cntr.is_deleted,
                    St_AsGeoJSON(cntr.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_landtype AS land ON land.id=cntr.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE cntr.year='{year}' AND cntr.type_id in ({land_type}) and rgn.id in ({region}) 
                    and dst.id in ({district}) and cntn.id in ({conton})
                    and cntr.is_deleted=false
                    GROUP BY "Type productivity", cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                             'land_type_id': i[2],
                                                                             'year': i[5], 'ink': i[3],
                                                                             'productivity': i[7], 'area_ha': i[6],
                                                                             'region_ru': i[8], 'region_ky': i[9],
                                                                             'region_en': i[10],
                                                                             'district_ru': i[11], 'district_ky': i[12],
                                                                             'district_en': i[13],
                                                                             'conton_ru': i[14], 'conton_ky': i[15],
                                                                             'conton_en': i[16],
                                                                             'land_type_ru': i[17],
                                                                             'land_type_ky': i[18],
                                                                             'land_type_en': i[19]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                               'land_type_id': i[2],
                                                                               'year': i[5], 'ink': i[3],
                                                                               'productivity': i[7], 'area_ha': i[6],
                                                                               'region_ru': i[8], 'region_ky': i[9],
                                                                               'region_en': i[10],
                                                                               'district_ru': i[11],
                                                                               'district_ky': i[12],
                                                                               'district_en': i[13],
                                                                               'conton_ru': i[14], 'conton_ky': i[15],
                                                                               'conton_en': i[16],
                                                                               'land_type_ru': i[17],
                                                                               'land_type_ky': i[18],
                                                                               'land_type_en': i[19]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif region and district and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (cntr.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id,
                    cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    cntr.year, cntr.area_ha, cntr.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    cntr.is_deleted,
                    St_AsGeoJSON(cntr.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_landtype AS land ON land.id=cntr.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE cntr.year='{year}' AND cntr.type_id in ({land_type}) and rgn.id in ({region}) 
                    and dst.id in ({district}) and cntr.is_deleted=false
                    GROUP BY "Type productivity", cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                             'land_type_id': i[2],
                                                                             'year': i[5], 'ink': i[3],
                                                                             'productivity': i[7], 'area_ha': i[6],
                                                                             'region_ru': i[8], 'region_ky': i[9],
                                                                             'region_en': i[10],
                                                                             'district_ru': i[11], 'district_ky': i[12],
                                                                             'district_en': i[13],
                                                                             'conton_ru': i[14], 'conton_ky': i[15],
                                                                             'conton_en': i[16],
                                                                             'land_type_ru': i[17],
                                                                             'land_type_ky': i[18],
                                                                             'land_type_en': i[19]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                               'land_type_id': i[2],
                                                                               'year': i[5], 'ink': i[3],
                                                                               'productivity': i[7], 'area_ha': i[6],
                                                                               'region_ru': i[8], 'region_ky': i[9],
                                                                               'region_en': i[10],
                                                                               'district_ru': i[11],
                                                                               'district_ky': i[12],
                                                                               'district_en': i[13],
                                                                               'conton_ru': i[14], 'conton_ky': i[15],
                                                                               'conton_en': i[16],
                                                                               'land_type_ru': i[17],
                                                                               'land_type_ky': i[18],
                                                                               'land_type_en': i[19]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif region and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (cntr.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id,
                    cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    cntr.year, cntr.area_ha, cntr.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    cntr.is_deleted,
                    St_AsGeoJSON(cntr.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_landtype AS land ON land.id=cntr.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE cntr.year='{year}' AND cntr.type_id in ({land_type}) and rgn.id in ({region})
                    and cntr.is_deleted=false
                    GROUP BY "Type productivity", cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                             'land_type_id': i[2],
                                                                             'year': i[5], 'ink': i[3],
                                                                             'productivity': i[7], 'area_ha': i[6],
                                                                             'region_ru': i[8], 'region_ky': i[9],
                                                                             'region_en': i[10],
                                                                             'district_ru': i[11], 'district_ky': i[12],
                                                                             'district_en': i[13],
                                                                             'conton_ru': i[14], 'conton_ky': i[15],
                                                                             'conton_en': i[16],
                                                                             'land_type_ru': i[17],
                                                                             'land_type_ky': i[18],
                                                                             'land_type_en': i[19]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                               'land_type_id': i[2],
                                                                               'year': i[5], 'ink': i[3],
                                                                               'productivity': i[7], 'area_ha': i[6],
                                                                               'region_ru': i[8], 'region_ky': i[9],
                                                                               'region_en': i[10],
                                                                               'district_ru': i[11],
                                                                               'district_ky': i[12],
                                                                               'district_en': i[13],
                                                                               'conton_ru': i[14], 'conton_ky': i[15],
                                                                               'conton_en': i[16],
                                                                               'land_type_ru': i[17],
                                                                               'land_type_ky': i[18],
                                                                               'land_type_en': i[19]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif district and conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (cntr.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id, 
                    cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    cntr.year, cntr.area_ha, cntr.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    cntr.is_deleted,
                    St_AsGeoJSON(cntr.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_landtype AS land ON land.id=cntr.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE cntr.year='{year}' AND cntr.type_id in ({land_type}) and dst.id in ({district})
                    and cntn.id in ({conton}) and cntr.is_deleted=false
                    GROUP BY "Type productivity", cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                         'land_type_id': i[2],
                                                                         'year': i[5], 'ink': i[3],
                                                                         'productivity': i[7], 'area_ha': i[6],
                                                                         'region_ru': i[8], 'region_ky': i[9],
                                                                         'region_en': i[10],
                                                                         'district_ru': i[11], 'district_ky': i[12],
                                                                         'district_en': i[13],
                                                                         'conton_ru': i[14], 'conton_ky': i[15],
                                                                         'conton_en': i[16],
                                                                         'land_type_ru': i[17],
                                                                         'land_type_ky': i[18],
                                                                         'land_type_en': i[19]},
                                       "geometry": eval(i[-1])})
                    if i[0] in 'productive':
                        pass
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                               'land_type_id': i[2],
                                                                               'year': i[5], 'ink': i[3],
                                                                               'productivity': i[7], 'area_ha': i[6],
                                                                               'region_ru': i[8], 'region_ky': i[9],
                                                                               'region_en': i[10],
                                                                               'district_ru': i[11],
                                                                               'district_ky': i[12],
                                                                               'district_en': i[13],
                                                                               'conton_ru': i[14], 'conton_ky': i[15],
                                                                               'conton_en': i[16],
                                                                               'land_type_ru': i[17],
                                                                               'land_type_ky': i[18],
                                                                               'land_type_en': i[19]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif district and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (cntr.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id,
                    cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    cntr.year, cntr.area_ha, cntr.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    cntr.is_deleted,
                    St_AsGeoJSON(cntr.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_landtype AS land ON land.id=cntr.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE cntr.year='{year}' AND cntr.type_id in ({land_type}) and dst.id in ({district})
                    and cntr.is_deleted=false
                    GROUP BY "Type productivity", cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                             'land_type_id': i[2],
                                                                             'year': i[5], 'ink': i[3],
                                                                             'productivity': i[7], 'area_ha': i[6],
                                                                             'region_ru': i[8], 'region_ky': i[9],
                                                                             'region_en': i[10],
                                                                             'district_ru': i[11], 'district_ky': i[12],
                                                                             'district_en': i[13],
                                                                             'conton_ru': i[14], 'conton_ky': i[15],
                                                                             'conton_en': i[16],
                                                                             'land_type_ru': i[17],
                                                                             'land_type_ky': i[18],
                                                                             'land_type_en': i[19]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                               'land_type_id': i[2],
                                                                               'year': i[5], 'ink': i[3],
                                                                               'productivity': i[7], 'area_ha': i[6],
                                                                               'region_ru': i[8], 'region_ky': i[9],
                                                                               'region_en': i[10],
                                                                               'district_ru': i[11],
                                                                               'district_ky': i[12],
                                                                               'district_en': i[13],
                                                                               'conton_ru': i[14], 'conton_ky': i[15],
                                                                               'conton_en': i[16],
                                                                               'land_type_ru': i[17],
                                                                               'land_type_ky': i[18],
                                                                               'land_type_en': i[19]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (cntr.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id,
                    cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    cntr.year, cntr.area_ha, cntr.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    cntr.is_deleted,
                    St_AsGeoJSON(cntr.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_landtype AS land ON land.id=cntr.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE cntr.year='{year}' AND cntr.type_id in ({land_type}) and cntn.id in ({conton})
                    and cntr.is_deleted=false
                    GROUP BY "Type productivity", cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                             'land_type_id': i[2],
                                                                             'year': i[5], 'ink': i[3],
                                                                             'productivity': i[7], 'area_ha': i[6],
                                                                             'region_ru': i[8], 'region_ky': i[9],
                                                                             'region_en': i[10],
                                                                             'district_ru': i[11], 'district_ky': i[12],
                                                                             'district_en': i[13],
                                                                             'conton_ru': i[14], 'conton_ky': i[15],
                                                                             'conton_en': i[16],
                                                                             'land_type_ru': i[17],
                                                                             'land_type_ky': i[18],
                                                                             'land_type_en': i[19]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                               'land_type_id': i[2],
                                                                               'year': i[5], 'ink': i[3],
                                                                               'productivity': i[7], 'area_ha': i[6],
                                                                               'region_ru': i[8], 'region_ky': i[9],
                                                                               'region_en': i[10],
                                                                               'district_ru': i[11],
                                                                               'district_ky': i[12],
                                                                               'district_en': i[13],
                                                                               'conton_ru': i[14], 'conton_ky': i[15],
                                                                               'conton_en': i[16],
                                                                               'land_type_ru': i[17],
                                                                               'land_type_ky': i[18],
                                                                               'land_type_en': i[19]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (cntr.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id,
                    cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    cntr.year, cntr.area_ha, cntr.productivity, 
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    cntr.is_deleted,
                    St_AsGeoJSON(cntr.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_landtype AS land ON land.id=cntr.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE cntr.year='{year}' AND cntr.type_id in ({land_type})
                    and cntr.is_deleted=false 
                    GROUP BY "Type productivity", cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                             'land_type_id': i[2],
                                                                             'year': i[5], 'ink': i[3],
                                                                             'productivity': i[7], 'area_ha': i[6],
                                                                             'region_ru': i[8], 'region_ky': i[9],
                                                                             'region_en': i[10],
                                                                             'district_ru': i[11], 'district_ky': i[12],
                                                                             'district_en': i[13],
                                                                             'conton_ru': i[14], 'conton_ky': i[15],
                                                                             'conton_en': i[16],
                                                                             'land_type_ru': i[17],
                                                                             'land_type_ky': i[18],
                                                                             'land_type_en': i[19]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[4],
                                                                               'land_type_id': i[2],
                                                                               'year': i[5], 'ink': i[3],
                                                                               'productivity': i[7], 'area_ha': i[6],
                                                                               'region_ru': i[8], 'region_ky': i[9],
                                                                               'region_en': i[10],
                                                                               'district_ru': i[11],
                                                                               'district_ky': i[12],
                                                                               'district_en': i[13],
                                                                               'conton_ru': i[14], 'conton_ky': i[15],
                                                                               'conton_en': i[16],
                                                                               'land_type_ru': i[17],
                                                                               'land_type_ky': i[18],
                                                                               'land_type_en': i[19]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        else:
            return Response(data={"message": "parameter 'year and land_type' is required"}, status=400)


class CoordinatesPolygonAPIView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        year = request.GET.get('year')
        land_type = request.GET.get('land_type')
        district = request.GET.get('district')
        conton = request.GET.get('conton')
        if region and district and conton:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT cntn.id, cntn.name, St_AsGeoJSON(cntn.polygon) AS polygon 
                               FROM gip_conton AS cntn
                               JOIN gip_district AS dst ON dst.id=cntn.district_id 
                               JOIN gip_region AS rgn ON rgn.id=dst.region_id  
                               WHERE rgn.id IN ({region}) AND dst.id IN ({district}) AND cntn.id IN ({conton})
                               GROUP BY cntn.id
                               ORDER BY cntn.id;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature", "properties": {'id': i[0], 'name': i[1]},
                                 "geometry": eval(i[-1]) if i[-1] else None})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": data}})
        elif region and district:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT dst.id, dst.name, St_AsGeoJSON(dst.polygon) AS polygon 
                               FROM gip_district AS dst 
                               JOIN gip_region AS rgn ON rgn.id=dst.region_id 
                               WHERE rgn.id IN ({region}) AND dst.id IN ({district})
                               GROUP BY dst.id
                               ORDER BY dst.id;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature", "properties": {'id': i[0], 'name': i[1]},
                                 "geometry": eval(i[-1]) if i[-1] else None})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": data}})
        elif region:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT rgn.id, rgn.name, St_AsGeoJSON(rgn.polygon) AS polygon 
                               FROM gip_region AS rgn
                               WHERE rgn.id IN ({region}) 
                               GROUP BY rgn.id
                               ORDER BY rgn.id;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature", "properties": {'id': i[0], 'name': i[1]},
                                 "geometry": eval(i[-1]) if i[-1] else None})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": data}})
        elif district and conton:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT cntn.id, cntn.name, St_AsGeoJSON(cntn.polygon) AS polygon 
                               FROM gip_conton as cntn 
                               JOIN gip_district AS dst ON dst.id=cntn.district_id 
                               JOIN gip_region AS rgn ON rgn.id=dst.region_id 
                               WHERE dst.id IN ({district}) AND cntn.id in ({conton})
                               GROUP BY cntn.id
                               ORDER BY cntn.id;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature", "properties": {'id': i[0], 'name': i[1]},
                                 "geometry": eval(i[-1]) if i[-1] else None})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": data}})
        elif district:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT dst.id, dst.name, St_AsGeoJSON(dst.polygon) AS polygon 
                               FROM gip_district AS dst
                               JOIN gip_region AS rgn ON rgn.id=dst.region_id 
                               WHERE dst.id IN ({district})
                               GROUP BY dst.id
                               ORDER BY dst.id;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature", "properties": {'id': i[0], 'name': i[1]},
                                 "geometry": eval(i[-1]) if i[-1] else None})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": data}})
        elif conton:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT cntn.id, cntn.name, St_AsGeoJSON(cntn.polygon) AS polygon 
                               FROM gip_conton AS cntn 
                               WHERE cntn.id IN ({conton})
                               GROUP BY cntn.id
                               ORDER BY cntn.id;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature", "properties": {'id': i[0], 'name': i[1]},
                                 "geometry": eval(i[-1]) if i[-1] else None})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": data}})
        else:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT rgn.id, rgn.name, St_AsGeoJSON(rgn.polygon) AS polygon 
                               FROM gip_region as rgn
                               GROUP BY rgn.id
                               ORDER BY rgn.id;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature", "properties": {'id': i[0], 'name': i[1]},
                                 "geometry": eval(i[-1]) if i[-1] else None})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": data}})


"""

  33938 |        24864 |             58 |               42 | f          | Иссык-Кульский район
"""
