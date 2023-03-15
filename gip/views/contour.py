from django.contrib.gis.geos import GEOSGeometry
from django.core import serializers
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters, status, mixins
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from gip.models.contour import Contour, ContourYear
from gip.pagination.contour_pagination import SearchContourPagination
from gip.serializers.contour import ContourSerializer, AuthDetailContourSerializer, AuthDetailContourYearSerializer
from gip.views.handbook_contour import contour_Kyrgyzstan


class AuthDetailContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all().order_by('id')
    serializer_class = AuthDetailContourSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        ContourYear.objects.filter(contour_id=instance.pk).update(is_deleted=True)
        instance.save()
        return Response('Contour and contour-year is deleted')


class AuthDetailContourYearViewSet(viewsets.ModelViewSet):
    queryset = ContourYear.objects.all()
    serializer_class = AuthDetailContourYearSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        intersect = ContourYear.objects.filter(
            polygon__intersects=GEOSGeometry(f"{serializer.initial_data['polygon']}"))
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT ST_Contains('{contour_Kyrgyzstan}'::geography::geometry, 
                '{GEOSGeometry(f"{serializer.initial_data['polygon']}")}'::geography::geometry);""")
            inside = cursor.fetchall()
            print(inside)
        if intersect:
            return Response("Пересекаются поля")
        elif not inside[0][0]:
            return Response("Создайте поле внутри Кыргызстана")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response('Contour-year is deleted')


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
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        year = request.GET.get('year')
        land_type = request.GET.get('land_type')
        district = request.GET.get('district')
        conton = request.GET.get('conton')
        if region and district and conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                               gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                               gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                               rgn.name_ru, rgn.name_ky, rgn.name_en,
                               dst.name_ru, dst.name_ky, dst.name_en,
                               cntn.name_ru, cntn.name_ky, cntn.name_en,
                               land.name_ru, land.name_ky, land.name_en,
                               St_AsGeoJSON(gcy.polygon) as polygon   
                               FROM gip_contour AS cntr 
                               JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                               JOIN gip_landtype AS land ON land.id=gcy.type_id
                               JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                               JOIN gip_district AS dst ON dst.id=cntn.district_id
                               JOIN gip_region AS rgn ON rgn.id=dst.region_id
                               where rgn.id in ({region}) and dst.id in ({district}) and cntn.id in ({conton}) 
                               and gcy.type_id in ({land_type}) and gcy.year='{year}' order by cntr.id;
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[4],
                                                                      'contour_year_id': i[1],
                                                                      'land_type_id': i[2],
                                                                      'contour_year_cs': i[5],
                                                                      'year': i[6], 'ink': i[3],
                                                                      'productivity': i[8], 'area_ha': i[7],
                                                                      'region_ru': i[9], 'region_ky': i[10],
                                                                      'region_en': i[11],
                                                                      'district_ru': i[12], 'district_ky': i[13],
                                                                      'district_en': i[14],
                                                                      'conton_ru': i[15], 'conton_ky': i[16],
                                                                      'conton_en': i[17],
                                                                      'land_type_ru': i[18], 'land_type_ky': i[19],
                                                                      'land_type_en': i[20]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif region and district and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                                gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                                rgn.name_ru, rgn.name_ky, rgn.name_en,
                                dst.name_ru, dst.name_ky, dst.name_en,
                                cntn.name_ru, cntn.name_ky, cntn.name_en,
                                land.name_ru, land.name_ky, land.name_en,
                                St_AsGeoJSON(gcy.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                                JOIN gip_landtype AS land ON land.id=gcy.type_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where gcy.type_id in ({land_type}) and rgn.id in ({region}) and gcy.year='{year}'
                                and dst.id in ({district}) order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[4],
                                                                      'contour_year_id': i[1],
                                                                      'land_type_id': i[2],
                                                                      'contour_year_cs': i[5],
                                                                      'year': i[6], 'ink': i[3],
                                                                      'productivity': i[8], 'area_ha': i[7],
                                                                      'region_ru': i[9], 'region_ky': i[10],
                                                                      'region_en': i[11],
                                                                      'district_ru': i[12], 'district_ky': i[13],
                                                                      'district_en': i[14],
                                                                      'conton_ru': i[15], 'conton_ky': i[16],
                                                                      'conton_en': i[17],
                                                                      'land_type_ru': i[18], 'land_type_ky': i[19],
                                                                      'land_type_en': i[20]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif region and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                                gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                                rgn.name_ru, rgn.name_ky, rgn.name_en,
                                dst.name_ru, dst.name_ky, dst.name_en,
                                cntn.name_ru, cntn.name_ky, cntn.name_en,
                                land.name_ru, land.name_ky, land.name_en,
                                St_AsGeoJSON(gcy.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                                JOIN gip_landtype AS land ON land.id=gcy.type_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where gcy.type_id in ({land_type}) and rgn.id in ({region}) and gcy.year='{year}'
                                order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[4],
                                                                      'contour_year_id': i[1],
                                                                      'land_type_id': i[2],
                                                                      'contour_year_cs': i[5],
                                                                      'year': i[6], 'ink': i[3],
                                                                      'productivity': i[8], 'area_ha': i[7],
                                                                      'region_ru': i[9], 'region_ky': i[10],
                                                                      'region_en': i[11],
                                                                      'district_ru': i[12], 'district_ky': i[13],
                                                                      'district_en': i[14],
                                                                      'conton_ru': i[15], 'conton_ky': i[16],
                                                                      'conton_en': i[17],
                                                                      'land_type_ru': i[18], 'land_type_ky': i[19],
                                                                      'land_type_en': i[20]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif district and conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                    SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                                    gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                    gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                                    dst.name_ru, dst.name_ky, dst.name_en,
                                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                                    land.name_ru, land.name_ky, land.name_en,
                                    St_AsGeoJSON(gcy.polygon) as polygon  
                                    FROM gip_contour AS cntr 
                                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                                    JOIN gip_landtype AS land ON land.id=gcy.type_id
                                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                    where gcy.type_id in ({land_type}) and dst.id in ({district}) and gcy.year='{year}'
                                    and cntn.id in ({conton}) order by cntr.id;
                                        """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[4],
                                                                      'contour_year_id': i[1],
                                                                      'land_type_id': i[2],
                                                                      'contour_year_cs': i[5],
                                                                      'year': i[6], 'ink': i[3],
                                                                      'productivity': i[8], 'area_ha': i[7],
                                                                      'region_ru': i[9], 'region_ky': i[10],
                                                                      'region_en': i[11],
                                                                      'district_ru': i[12], 'district_ky': i[13],
                                                                      'district_en': i[14],
                                                                      'conton_ru': i[15], 'conton_ky': i[16],
                                                                      'conton_en': i[17],
                                                                      'land_type_ru': i[18], 'land_type_ky': i[19],
                                                                      'land_type_en': i[20]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif district and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                                gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                                rgn.name_ru, rgn.name_ky, rgn.name_en,
                                dst.name_ru, dst.name_ky, dst.name_en,
                                cntn.name_ru, cntn.name_ky, cntn.name_en,
                                land.name_ru, land.name_ky, land.name_en,
                                St_AsGeoJSON(gcy.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                                JOIN gip_landtype AS land ON land.id=gcy.type_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where gcy.type_id in ({land_type}) and gcy.year='{year}' and dst.id in ({district}) 
                                order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[4],
                                                                      'contour_year_id': i[1],
                                                                      'land_type_id': i[2],
                                                                      'contour_year_cs': i[5],
                                                                      'year': i[6], 'ink': i[3],
                                                                      'productivity': i[8], 'area_ha': i[7],
                                                                      'region_ru': i[9], 'region_ky': i[10],
                                                                      'region_en': i[11],
                                                                      'district_ru': i[12], 'district_ky': i[13],
                                                                      'district_en': i[14],
                                                                      'conton_ru': i[15], 'conton_ky': i[16],
                                                                      'conton_en': i[17],
                                                                      'land_type_ru': i[18], 'land_type_ky': i[19],
                                                                      'land_type_en': i[20]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                               gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                               gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                               rgn.name_ru, rgn.name_ky, rgn.name_en,
                               dst.name_ru, dst.name_ky, dst.name_en,
                               cntn.name_ru, cntn.name_ky, cntn.name_en,
                               land.name_ru, land.name_ky, land.name_en,
                               St_AsGeoJSON(gcy.polygon) as polygon    
                               FROM gip_contour AS cntr 
                               JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                               JOIN gip_landtype AS land ON land.id=gcy.type_id
                               JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                               JOIN gip_district AS dst ON dst.id=cntn.district_id
                               JOIN gip_region AS rgn ON rgn.id=dst.region_id
                               where cntn.id in ({conton}) and gcy.type_id in ({land_type}) and gcy.year='{year}' 
                               order by cntr.id;
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[4],
                                                                      'contour_year_id': i[1],
                                                                      'land_type_id': i[2],
                                                                      'contour_year_cs': i[5],
                                                                      'year': i[6], 'ink': i[3],
                                                                      'productivity': i[8], 'area_ha': i[7],
                                                                      'region_ru': i[9], 'region_ky': i[10],
                                                                      'region_en': i[11],
                                                                      'district_ru': i[12], 'district_ky': i[13],
                                                                      'district_en': i[14],
                                                                      'conton_ru': i[15], 'conton_ky': i[16],
                                                                      'conton_en': i[17],
                                                                      'land_type_ru': i[18], 'land_type_ky': i[19],
                                                                      'land_type_en': i[20]},
                                                       "geometry": eval(i[-1])}]}})
                return Response(data)
        elif year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                                gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                                rgn.name_ru, rgn.name_ky, rgn.name_en,
                                dst.name_ru, dst.name_ky, dst.name_en,
                                cntn.name_ru, cntn.name_ky, cntn.name_en,
                                land.name_ru, land.name_ky, land.name_en,
                                St_AsGeoJSON(gcy.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                                JOIN gip_landtype AS land ON land.id=gcy.type_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where gcy.year='{year}' and gcy.type_id in ({land_type})
                                order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                        "contour_year": {"type": "FeatureCollection",
                                         "features": [{"type": "Feature",
                                                       "properties": {'contour_id': i[0], 'contour_cs': i[4],
                                                                      'contour_year_id': i[1],
                                                                      'land_type_id': i[2],
                                                                      'contour_year_cs': i[5],
                                                                      'year': i[6], 'ink': i[3],
                                                                      'productivity': i[8], 'area_ha': i[7],
                                                                      'region_ru': i[9], 'region_ky': i[10],
                                                                      'region_en': i[11],
                                                                      'district_ru': i[12], 'district_ky': i[13],
                                                                      'district_en': i[14],
                                                                      'conton_ru': i[15], 'conton_ky': i[16],
                                                                      'conton_en': i[17],
                                                                      'land_type_ru': i[18], 'land_type_ky': i[19],
                                                                      'land_type_en': i[20]},
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
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        year = request.GET.get('year')
        land_type = request.GET.get('land_type')
        district = request.GET.get('district')
        conton = request.GET.get('conton')
        if region and district and conton and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end)) as "Productive",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "productive_pct",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "unproductive_pct",
                    cntn.name
                    FROM gip_contour AS cntr 
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where gcy.year='{year}' and gcy.type_id in ({land_type}) and cntn.id in ({conton}) 
                    and rgn.id in ({region}) and dst.id in ({district})
                    group by cntn.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'Conton': i[-1], 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif region and district and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end)) as "Productive",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "productive_pct",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "unproductive_pct",
                    cntn.name
                    FROM gip_contour AS cntr 
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where rgn.id in ({region}) and gcy.type_id in ({land_type}) and gcy.year='{year}' and dst.id in ({district})
                    group by cntn.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'Conton': i[-1], 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif region and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end)) as "Productive",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "productive_pct",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "unproductive_pct",
                    dst.name
                    FROM gip_contour AS cntr 
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where rgn.id in ({region}) and gcy.type_id in ({land_type}) and gcy.year='{year}'
                    group by dst.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'District': i[-1], 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif district and conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end)) as "Productive",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "productive_pct",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "unproductive_pct",
                    cntn.name
                    FROM gip_contour AS cntr 
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    where gcy.year='{year}' and gcy.type_id in ({land_type}) and dst.id in ({district}) 
                    and cntn.id in ({conton}) group by cntn.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'Conton': i[-1], 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif district and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end)) as "Productive",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "productive_pct",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "unproductive_pct",
                    cntn.name 
                    FROM gip_contour AS cntr 
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where gcy.year='{year}' and gcy.type_id in ({land_type}) and dst.id in ({district})
                    group by cntn.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'Conton': i[-1], 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end)) as "Productive",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "productive_pct",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "unproductive_pct",
                    cntn.name 
                    FROM gip_contour AS cntr 
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where gcy.year='{year}' and gcy.type_id in ({land_type}) and cntn.id in ({conton})
                    group by cntn.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'Conton': i[-1], 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                return Response(data)
        elif year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT 
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end)) as "Productive",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                    round(sum(case when (gcy.productivity)::float >= 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "productive_pct",
                    round(sum(case when (gcy.productivity)::float < 1.6 then gcy.area_ha else 0 end) / sum(gcy.area_ha) * 100) as "unproductive_pct",
                    rgn.name 
                    FROM gip_contour AS cntr  
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    where gcy.year='{year}' and gcy.type_id in ({land_type})
                    group by rgn.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'Region': i[-1], 'Productive': {'ha': i[0], 'percent': i[2]},
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
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        year = request.GET.get('year')
        land_type = request.GET.get('land_type')
        district = request.GET.get('district')
        conton = request.GET.get('conton')
        if region and district and conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (gcy.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id, gcy.id AS contour_year_id, 
                    gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    St_AsGeoJSON(gcy.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_landtype AS land ON land.id=gcy.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE gcy.year='{year}' AND gcy.type_id in ({land_type}) and rgn.id in ({region}) 
                    and dst.id in ({district}) and cntn.id in ({conton})
                    GROUP BY "Type productivity", gcy.id, cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                             'contour_year_id': i[2],
                                                                             'land_type_id': i[3],
                                                                             'contour_year_cs': i[6],
                                                                             'year': i[7], 'ink': i[3],
                                                                             'productivity': i[9], 'area_ha': i[8],
                                                                             'region_ru': i[10], 'region_ky': i[11],
                                                                             'region_en': i[12],
                                                                             'district_ru': i[13], 'district_ky': i[14],
                                                                             'district_en': i[15],
                                                                             'conton_ru': i[16], 'conton_ky': i[17],
                                                                             'conton_en': i[18],
                                                                             'land_type_ru': i[19],
                                                                             'land_type_ky': i[20],
                                                                             'land_type_en': i[21]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                               'contour_year_id': i[2],
                                                                               'land_type_id': i[3],
                                                                               'contour_year_cs': i[6],
                                                                               'year': i[7], 'ink': i[3],
                                                                               'productivity': i[9], 'area_ha': i[8],
                                                                               'region_ru': i[10], 'region_ky': i[11],
                                                                               'region_en': i[12],
                                                                               'district_ru': i[13],
                                                                               'district_ky': i[14],
                                                                               'district_en': i[15],
                                                                               'conton_ru': i[16], 'conton_ky': i[17],
                                                                               'conton_en': i[18],
                                                                               'land_type_ru': i[19],
                                                                               'land_type_ky': i[20],
                                                                               'land_type_en': i[21]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif region and district and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (gcy.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id, gcy.id AS contour_year_id, 
                    gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    St_AsGeoJSON(gcy.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_landtype AS land ON land.id=gcy.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE gcy.year='{year}' AND gcy.type_id in ({land_type}) and rgn.id in ({region}) 
                    and dst.id in ({district}) GROUP BY "Type productivity", gcy.id, cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                             'contour_year_id': i[2],
                                                                             'land_type_id': i[3],
                                                                             'contour_year_cs': i[6],
                                                                             'year': i[7], 'ink': i[3],
                                                                             'productivity': i[9], 'area_ha': i[8],
                                                                             'region_ru': i[10], 'region_ky': i[11],
                                                                             'region_en': i[12],
                                                                             'district_ru': i[13], 'district_ky': i[14],
                                                                             'district_en': i[15],
                                                                             'conton_ru': i[16], 'conton_ky': i[17],
                                                                             'conton_en': i[18],
                                                                             'land_type_ru': i[19],
                                                                             'land_type_ky': i[20],
                                                                             'land_type_en': i[21]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                               'contour_year_id': i[2],
                                                                               'land_type_id': i[3],
                                                                               'contour_year_cs': i[6],
                                                                               'year': i[7], 'ink': i[3],
                                                                               'productivity': i[9], 'area_ha': i[8],
                                                                               'region_ru': i[10], 'region_ky': i[11],
                                                                               'region_en': i[12],
                                                                               'district_ru': i[13],
                                                                               'district_ky': i[14],
                                                                               'district_en': i[15],
                                                                               'conton_ru': i[16], 'conton_ky': i[17],
                                                                               'conton_en': i[18],
                                                                               'land_type_ru': i[19],
                                                                               'land_type_ky': i[20],
                                                                               'land_type_en': i[21]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif region and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (gcy.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id, gcy.id AS contour_year_id, 
                    gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en, 
                    St_AsGeoJSON(gcy.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_landtype AS land ON land.id=gcy.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE gcy.year='{year}' AND gcy.type_id in ({land_type}) and rgn.id in ({region}) 
                    GROUP BY "Type productivity", gcy.id, cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                             'contour_year_id': i[2],
                                                                             'land_type_id': i[3],
                                                                             'contour_year_cs': i[6],
                                                                             'year': i[7], 'ink': i[3],
                                                                             'productivity': i[9], 'area_ha': i[8],
                                                                             'region_ru': i[10], 'region_ky': i[11],
                                                                             'region_en': i[12],
                                                                             'district_ru': i[13], 'district_ky': i[14],
                                                                             'district_en': i[15],
                                                                             'conton_ru': i[16], 'conton_ky': i[17],
                                                                             'conton_en': i[18],
                                                                             'land_type_ru': i[19],
                                                                             'land_type_ky': i[20],
                                                                             'land_type_en': i[21]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                               'contour_year_id': i[2],
                                                                               'land_type_id': i[3],
                                                                               'contour_year_cs': i[6],
                                                                               'year': i[7], 'ink': i[3],
                                                                               'productivity': i[9], 'area_ha': i[8],
                                                                               'region_ru': i[10], 'region_ky': i[11],
                                                                               'region_en': i[12],
                                                                               'district_ru': i[13],
                                                                               'district_ky': i[14],
                                                                               'district_en': i[15],
                                                                               'conton_ru': i[16], 'conton_ky': i[17],
                                                                               'conton_en': i[18],
                                                                               'land_type_ru': i[19],
                                                                               'land_type_ky': i[20],
                                                                               'land_type_en': i[21]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif district and conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (gcy.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id, gcy.id AS contour_year_id, 
                    gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    St_AsGeoJSON(gcy.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_landtype AS land ON land.id=gcy.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE gcy.year='{year}' AND gcy.type_id in ({land_type}) and dst.id in ({district})
                    and cntn.id in ({conton}) 
                    GROUP BY "Type productivity", gcy.id, cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                         'contour_year_id': i[2],
                                                                         'land_type_id': i[3],
                                                                         'contour_year_cs': i[6],
                                                                         'year': i[7], 'ink': i[3],
                                                                         'productivity': i[9], 'area_ha': i[8],
                                                                         'region_ru': i[10], 'region_ky': i[11],
                                                                         'region_en': i[12],
                                                                         'district_ru': i[13], 'district_ky': i[14],
                                                                         'district_en': i[15],
                                                                         'conton_ru': i[16], 'conton_ky': i[17],
                                                                         'conton_en': i[18],
                                                                         'land_type_ru': i[19], 'land_type_ky': i[20],
                                                                         'land_type_en': i[21]},
                                       "geometry": eval(i[-1])})
                    if i[0] in 'productive':
                        pass
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                               'contour_year_id': i[2],
                                                                               'land_type_id': i[3],
                                                                               'contour_year_cs': i[6],
                                                                               'year': i[7], 'ink': i[3],
                                                                               'productivity': i[9], 'area_ha': i[8],
                                                                               'region_ru': i[10], 'region_ky': i[11],
                                                                               'region_en': i[12],
                                                                               'district_ru': i[13],
                                                                               'district_ky': i[14],
                                                                               'district_en': i[15],
                                                                               'conton_ru': i[16], 'conton_ky': i[17],
                                                                               'conton_en': i[18],
                                                                               'land_type_ru': i[19],
                                                                               'land_type_ky': i[20],
                                                                               'land_type_en': i[21]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif district and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (gcy.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id, gcy.id AS contour_year_id, 
                    gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    St_AsGeoJSON(gcy.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_landtype AS land ON land.id=gcy.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE gcy.year='{year}' AND gcy.type_id in ({land_type}) and dst.id in ({district})
                    GROUP BY "Type productivity", gcy.id, cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                             'contour_year_id': i[2],
                                                                             'land_type_id': i[3],
                                                                             'contour_year_cs': i[6],
                                                                             'year': i[7], 'ink': i[3],
                                                                             'productivity': i[9], 'area_ha': i[8],
                                                                             'region_ru': i[10], 'region_ky': i[11],
                                                                             'region_en': i[12],
                                                                             'district_ru': i[13], 'district_ky': i[14],
                                                                             'district_en': i[15],
                                                                             'conton_ru': i[16], 'conton_ky': i[17],
                                                                             'conton_en': i[18],
                                                                             'land_type_ru': i[19],
                                                                             'land_type_ky': i[20],
                                                                             'land_type_en': i[21]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                               'contour_year_id': i[2],
                                                                               'land_type_id': i[3],
                                                                               'contour_year_cs': i[6],
                                                                               'year': i[7], 'ink': i[3],
                                                                               'productivity': i[9], 'area_ha': i[8],
                                                                               'region_ru': i[10], 'region_ky': i[11],
                                                                               'region_en': i[12],
                                                                               'district_ru': i[13],
                                                                               'district_ky': i[14],
                                                                               'district_en': i[15],
                                                                               'conton_ru': i[16], 'conton_ky': i[17],
                                                                               'conton_en': i[18],
                                                                               'land_type_ru': i[19],
                                                                               'land_type_ky': i[20],
                                                                               'land_type_en': i[21]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif conton and year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (gcy.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id, gcy.id AS contour_year_id, 
                    gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity,
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    St_AsGeoJSON(gcy.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_landtype AS land ON land.id=gcy.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE gcy.year='{year}' AND gcy.type_id in ({land_type}) and cntn.id in ({conton})
                    GROUP BY "Type productivity", gcy.id, cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                             'contour_year_id': i[2],
                                                                             'land_type_id': i[3],
                                                                             'contour_year_cs': i[6],
                                                                             'year': i[7], 'ink': i[3],
                                                                             'productivity': i[9], 'area_ha': i[8],
                                                                             'region_ru': i[10], 'region_ky': i[11],
                                                                             'region_en': i[12],
                                                                             'district_ru': i[13], 'district_ky': i[14],
                                                                             'district_en': i[15],
                                                                             'conton_ru': i[16], 'conton_ky': i[17],
                                                                             'conton_en': i[18],
                                                                             'land_type_ru': i[19],
                                                                             'land_type_ky': i[20],
                                                                             'land_type_en': i[21]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                               'contour_year_id': i[2],
                                                                               'land_type_id': i[3],
                                                                               'contour_year_cs': i[6],
                                                                               'year': i[7], 'ink': i[3],
                                                                               'productivity': i[9], 'area_ha': i[8],
                                                                               'region_ru': i[10], 'region_ky': i[11],
                                                                               'region_en': i[12],
                                                                               'district_ru': i[13],
                                                                               'district_ky': i[14],
                                                                               'district_en': i[15],
                                                                               'conton_ru': i[16], 'conton_ky': i[17],
                                                                               'conton_en': i[18],
                                                                               'land_type_ru': i[19],
                                                                               'land_type_ky': i[20],
                                                                               'land_type_en': i[21]},
                                             'geometry': eval(i[-1])})
                return Response({"productive": {"type": "FeatureCollection",
                                                "features": productive},
                                 "unproductive": {"type": "FeatureCollection",
                                                  "features": unproductive}})
        elif year and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT CASE WHEN (gcy.productivity)::float >= 1.6 THEN 'productive'
                    ELSE 'unproductive' END AS "Type productivity", cntr.id AS contour_id, gcy.id AS contour_year_id, 
                    gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                    gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, gcy.productivity, 
                    rgn.name_ru, rgn.name_ky, rgn.name_en,
                    dst.name_ru, dst.name_ky, dst.name_en,
                    cntn.name_ru, cntn.name_ky, cntn.name_en,
                    land.name_ru, land.name_ky, land.name_en,
                    St_AsGeoJSON(gcy.polygon) as polygon
                    FROM gip_contour AS cntr
                    JOIN gip_contouryear AS gcy ON gcy.contour_id=cntr.id
                    JOIN gip_landtype AS land ON land.id=gcy.type_id
                    JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                    JOIN gip_district AS dst ON dst.id=cntn.district_id
                    JOIN gip_region AS rgn ON rgn.id=dst.region_id
                    WHERE gcy.year='{year}' AND gcy.type_id in ({land_type}) 
                    GROUP BY "Type productivity", gcy.id, cntr.id, rgn.id, dst.id, cntn.id, land.id;""")
                rows = cursor.fetchall()
                productive = []
                unproductive = []
                for i in rows:
                    if i[0] in 'productive':
                        productive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                             'contour_year_id': i[2],
                                                                             'land_type_id': i[3],
                                                                             'contour_year_cs': i[6],
                                                                             'year': i[7], 'ink': i[3],
                                                                             'productivity': i[9], 'area_ha': i[8],
                                                                             'region_ru': i[10], 'region_ky': i[11],
                                                                             'region_en': i[12],
                                                                             'district_ru': i[13], 'district_ky': i[14],
                                                                             'district_en': i[15],
                                                                             'conton_ru': i[16], 'conton_ky': i[17],
                                                                             'conton_en': i[18],
                                                                             'land_type_ru': i[19],
                                                                             'land_type_ky': i[20],
                                                                             'land_type_en': i[21]},
                                           "geometry": eval(i[-1])})
                    else:
                        unproductive.append({"type": "Feature", "properties": {'contour_id': i[1], 'contour_cs': i[5],
                                                                               'contour_year_id': i[2],
                                                                               'land_type_id': i[3],
                                                                               'contour_year_cs': i[6],
                                                                               'year': i[7], 'ink': i[3],
                                                                               'productivity': i[9], 'area_ha': i[8],
                                                                               'region_ru': i[10], 'region_ky': i[11],
                                                                               'region_en': i[12],
                                                                               'district_ru': i[13],
                                                                               'district_ky': i[14],
                                                                               'district_en': i[15],
                                                                               'conton_ru': i[16], 'conton_ky': i[17],
                                                                               'conton_en': i[18],
                                                                               'land_type_ru': i[19],
                                                                               'land_type_ky': i[20],
                                                                               'land_type_en': i[21]},
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
