from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models.contour import Contour
from gip.pagination.contour_pagination import SearchContourPagination
from gip.serializers.contour import ContourSerializer, AuthDetailContourSerializer, UpdateAuthDetailContourSerializer


class AuthDetailContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all().order_by('id').filter(is_deleted=False)
    serializer_class = AuthDetailContourSerializer

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

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


class ContourSearchAPIView(ListAPIView):
    queryset = Contour.objects.filter(is_deleted=False)
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
            openapi.Parameter('culture', openapi.IN_QUERY, description="Culture", type=openapi.TYPE_INTEGER),
            openapi.Parameter('ai', openapi.IN_QUERY, description="AI", type=openapi.TYPE_BOOLEAN),
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
        culture = request.GET.get('culture')
        if land_type and year:
            if ai:
                sql = f"""
                SELECT cntr.id AS contour_id, cntr.type_id AS land_type_id, cntr.year, 
                cntr.area_ha, cntr.productivity,
                rgn.name_ru, rgn.name_ky, rgn.name_en,
                dst.name_ru, dst.name_ky, dst.name_en,
                land.name_ru, land.name_ky, land.name_en,
                clt.name_ru, clt.name_ky, clt.name_en, 
                St_AsGeoJSON(cntr.polygon) as polygon   
                FROM ai_contour_ai AS cntr
                JOIN gip_landtype AS land ON land.id=cntr.type_id
                JOIN gip_culture AS clt ON clt.id=cntr.culture_id
                JOIN gip_district AS dst ON dst.id=cntr.district_id
                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                WHERE cntr.type_id in ({land_type}) and cntr.year='{year}' and cntr.is_deleted=false
                and cntr.id > 11016
                """
                if region:
                    sql += f' and rgn.id in ({region})'
                if district:
                    sql += f' and dst.id in ({district})'
                if culture:
                    sql += f' and cntr.culture_id={culture}'
                sql += ' order by cntr.id;'
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    data = []
                    for i in rows:
                        data.append({
                            "contour_year": {"type": "FeatureCollection",
                                             "features": [{"type": "Feature",
                                                           "properties": {'contour_id': i[0], 'land_type_id': i[1],
                                                                          'year': i[2], 'area_ha': i[3],
                                                                          'productivity': i[4],
                                                                          'region_ru': i[5], 'region_ky': i[6],
                                                                          'region_en': i[7],
                                                                          'district_ru': i[8], 'district_ky': i[9],
                                                                          'district_en': i[10],
                                                                          'land_type_ru': i[11], 'land_type_ky': i[12],
                                                                          'land_type_en': i[13],
                                                                          'culture_ru': i[14], 'culture_ky': i[15],
                                                                          'culture_en': i[16]},
                                                           "geometry": eval(i[-1])}]}})
                    return Response(data)
            else:
                sql = f"""
                SELECT cntr.id AS contour_id, 
                cntr.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                cntr.year, cntr.area_ha, cntr.productivity,
                rgn.name_ru, rgn.name_ky, rgn.name_en,
                dst.name_ru, dst.name_ky, dst.name_en,
                cntn.name_ru, cntn.name_ky, cntn.name_en,
                land.name_ru, land.name_ky, land.name_en,
                clt.name_ru, clt.name_ky, clt.name_en,
                St_AsGeoJSON(cntr.polygon) as polygon   
                FROM gip_contour AS cntr 
                JOIN gip_landtype AS land ON land.id=cntr.type_id
                JOIN gip_culture AS clt ON clt.id=cntr.culture_id
                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                JOIN gip_district AS dst ON dst.id=cntn.district_id
                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                where cntr.type_id in ({land_type}) and cntr.year='{year}' and cntr.is_deleted=false
                """
                if region:
                    sql += f' and rgn.id in ({region})'
                if district:
                    sql += f' and dst.id in ({district})'
                if conton:
                    sql += f' and cntn.id in ({conton})'
                if culture:
                    sql += f' and cntr.culture_id={culture}'
                sql += ' order by cntr.id;'
                with connection.cursor() as cursor:
                    cursor.execute(sql)
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
                                                                          'land_type_en': i[18],
                                                                          'culture_ru': i[19], 'culture_ky': i[20],
                                                                          'culture_en': i[21]},
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
                  where rgn.id in ({region}) and cntr.type_id=1 and cntr.is_deleted=false and (cl.id in ({culture}))) as temp
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
                  where rgn.id in ({region}) and cntr.is_deleted=false and cntr.type_id=1) as temp
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
        if year and land_type:
            start = f"""SELECT
            round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end)) as "Productive",
            round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end)) as "Unproductive",
            round(sum(case when (cntr.productivity)::float >= 1.6 then cntr.area_ha else 0 end) / sum(cntr.area_ha) * 100) as "productive_pct",
            round(sum(case when (cntr.productivity)::float < 1.6 then cntr.area_ha else 0 end) / sum(cntr .area_ha) * 100) as "unproductive_pct",
            cntr.is_deleted, rgn.name_ru, rgn.name_ky, rgn.name_en
            """
            middle = f"""FROM gip_contour AS cntr
            JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
            JOIN gip_district AS dst ON dst.id=cntn.district_id
            JOIN gip_region AS rgn ON rgn.id=dst.region_id
            where cntr.is_deleted=false and cntr.year='{year}' and cntr.type_id={land_type}
            """
            end = 'group by cntr.is_deleted, rgn.name_ru, rgn.name_ky, rgn.name_en'
            parent = 'Country'
            child = 'Region'
            if region:
                start += ', dst.name_ru, dst.name_ky, dst.name_en '
                middle += f' and rgn.id in ({region})'
                end += ', dst.name_ru, dst.name_ky, dst.name_en'
                parent = 'Region'
                child = 'District'
            if district:
                start += ', dst.name_ru, dst.name_ky, dst.name_en, cntn.name_ru, cntn.name_ky, cntn.name_en '
                middle += f' and dst.id in ({district})'
                end += ', dst.name_ru, dst.name_ky, dst.name_en, cntn.name_ru, cntn.name_ky, cntn.name_en'
                parent = 'District'
                child = 'Conton'
            if conton:
                start += ', cntn.name_ru, cntn.name_ky, cntn.name_en '
                middle += f' and cntn.id in ({conton})'
                end += ', cntn.name_ru, cntn.name_ky, cntn.name_en'
                parent = 'Conton'
                child = 'Conton'
            sql = start + middle + end + ';'
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                total = sum([row[0] for row in rows]) + sum([row[1] for row in rows])
                data = []
                for i in rows:
                    data.append({'name_ru': i[-3], 'name_ky': i[-2], 'name_en': i[-1],
                                 'type': child, 'Productive': {'ha': i[0], 'percent': i[2]},
                                 'Unproductive': {'ha': i[1], 'percent': i[3]}})
                if rows:
                    if parent == 'Country':
                        responce = {
                            "name_ru": 'Кыргызстан',
                            "name_ky": 'Кыргызстан',
                            "name_en": 'Kyrgyzstan',
                            "type": parent,
                            'Productive': {'ha': sum([row[0] for row in rows]),
                                           'percent': round(sum([row[0] for row in rows]) / total * 100)},
                            "Unproductive": {
                                "ha": sum([row[1] for row in rows]),
                                "percent": round(sum([row[1] for row in rows]) / total * 100)
                            },
                            "Children": data
                        }
                    elif parent == child:
                        responce = {
                            'name_ru': i[-3], 'name_ky': i[-2], 'name_en': i[-1],
                            'type': child, 'Productive': {'ha': i[0], 'percent': i[2]},
                            'Unproductive': {'ha': i[1], 'percent': i[3]}
                        }
                    else:
                        responce = {
                            "name_ru": rows[0][5],
                            "name_ky": rows[0][6],
                            "name_en": rows[0][7],
                            "type": parent,
                            'Productive': {'ha': sum([row[0] for row in rows]),
                                           'percent': round(sum([row[0] for row in rows]) / total * 100)},
                            "Unproductive": {
                                "ha": sum([row[1] for row in rows]),
                                "percent": round(sum([row[1] for row in rows]) / total * 100)
                            },
                            "Children": data
                        }
                    return Response(responce)
                else:
                    return Response({})
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
                    land.name_ru, land.name_ky, land.name_en
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


class CultureStatisticsAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="Year", type=openapi.TYPE_INTEGER),
            openapi.Parameter('land_type', openapi.IN_QUERY, description="Land type", type=openapi.TYPE_INTEGER),
            openapi.Parameter('region', openapi.IN_QUERY, description="Region", type=openapi.TYPE_INTEGER),
            openapi.Parameter('district', openapi.IN_QUERY, description="District", type=openapi.TYPE_INTEGER),
            openapi.Parameter('conton', openapi.IN_QUERY, description="Conton", type=openapi.TYPE_INTEGER),
            openapi.Parameter('culture', openapi.IN_QUERY, description="Culture", type=openapi.TYPE_INTEGER),
            openapi.Parameter('ai', openapi.IN_QUERY, description="AI", type=openapi.TYPE_BOOLEAN),
        ],
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'culture_name_ru': openapi.Schema(type=openapi.TYPE_STRING),
                    'culture_name_ky': openapi.Schema(type=openapi.TYPE_STRING),
                    'culture_name_en': openapi.Schema(type=openapi.TYPE_STRING),
                    'area_ha': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'productivity': openapi.Schema(type=openapi.TYPE_NUMBER),
                    'territory_ru': openapi.Schema(type=openapi.TYPE_STRING),
                    'territory_ky': openapi.Schema(type=openapi.TYPE_STRING),
                    'territory_en': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        year = request.GET.get('year')
        land_type = request.GET.get('land_type')
        culture = request.GET.get('culture')
        region = request.GET.get('region')
        district = request.GET.get('district')
        conton = request.GET.get('conton')
        ai = request.GET.get('ai')
        if land_type and year:
            if ai:
                start = 'select culture_name_ru, culture_name_ky, culture_name_en, sum(area_ha) as total_area_ha, c'
                middle = f""" from (
                                      select clt.name_ru as culture_name_ru,
                                      clt.name_ky as culture_name_ky,
                                      clt.name_en as culture_name_en,
                                      area_ha, clt.coefficient_crop as c,
                                      rgn.name_ru as region_name_ru,
                                      rgn.name_ky as region_name_ky,
                                      rgn.name_en as region_name_en,
                                      dst.name_ru as district_name_ru,
                                      dst.name_ky as district_name_ky,
                                      dst.name_en as district_name_en
                                      from ai_contour_ai as cntr
                                      join gip_culture as clt on clt.id=cntr.culture_id
                                      JOIN gip_district AS dst ON dst.id=cntr.district_id
                                      JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                      where cntr.type_id in ({land_type}) and cntr.year='{year}' and cntr.is_deleted=false
                                      """
                end = ') as temp group by culture_name_ru, culture_name_ky, culture_name_en , c'
                if culture:
                    middle += f' and clt.id={culture}'
                if region:
                    start += ', region_name_ru, region_name_ky, region_name_en'
                    middle += f' and rgn.id in ({region})'
                    end += ', region_name_ru, region_name_ky, region_name_en'
                if district:
                    start += ', district_name_ru, district_name_ky, district_name_en'
                    middle += f' and dst.id in ({district})'
                    end += ', district_name_ru, district_name_ky, district_name_en'
                sql = start + middle + end + ';'
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    data = []
                    for i in rows:
                        if len(i) > 5:
                            data.append({'culture_name_ru': i[0], 'culture_name_ky': i[1], "culture_name_en": i[2],
                                         'area_ha': i[3], 'productivity': i[4] * i[3],
                                         "territory_ru": i[-3], "territory_ky": i[-2], "territory_en": i[-1]})
                        else:
                            data.append({'culture_name_ru': i[0], 'culture_name_ky': i[1], "culture_name_en": i[2],
                                         'area_ha': i[3], 'productivity': i[4],
                                         "territory_ru": 'Кыргызстан', "territory_ky": 'Кыргызстан',
                                         "territory_en": 'Kyrgyzstan'})
                    return Response(data)
            else:
                start = 'select culture_name_ru, culture_name_ky, culture_name_en, sum(area_ha) as total_area_ha, c'
                middle= f""" from (
                      select clt.name_ru as culture_name_ru,
                      clt.name_ky as culture_name_ky,
                      clt.name_en as culture_name_en,
                      area_ha, clt.coefficient_crop as c,
                      rgn.name_ru as region_name_ru,
                      rgn.name_ky as region_name_ky,
                      rgn.name_en as region_name_en,
                      dst.name_ru as district_name_ru,
                      dst.name_ky as district_name_ky,
                      dst.name_en as district_name_en,
                      cntn.name_ru as conton_name_ru,
                      cntn.name_ky as conton_name_ky,
                      cntn.name_en as conton_name_en 
                      from gip_contour as cntr
                      join gip_culture as clt on clt.id=cntr.culture_id
                      JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                      JOIN gip_district AS dst ON dst.id=cntn.district_id
                      JOIN gip_region AS rgn ON rgn.id=dst.region_id
                      where cntr.type_id in ({land_type}) and cntr.year='{year}' and cntr.is_deleted=false
                      """
                end = ') as temp group by culture_name_ru, culture_name_ky, culture_name_en, c'
                if culture:
                    middle += f' and clt.id={culture}'
                if region:
                    start += ', region_name_ru, region_name_ky, region_name_en'
                    middle += f' and rgn.id in ({region})'
                    end += ', region_name_ru, region_name_ky, region_name_en'
                if district:
                    start += ', district_name_ru, district_name_ky, district_name_en'
                    middle += f' and dst.id in ({district})'
                    end += ', district_name_ru, district_name_ky, district_name_en'
                if conton:
                    start += ', conton_name_ru, conton_name_ky, conton_name_en'
                    middle += f' and cntn.id in ({conton})'
                    end += ', conton_name_ru, conton_name_ky, conton_name_en'
                sql = start + middle + end + ';'
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    data = []
                    for i in rows:
                        if len(i) > 5:
                            data.append({'culture_name_ru': i[0], 'culture_name_ky': i[1], "culture_name_en": i[2],
                                         'area_ha': i[3], 'productivity': i[4] * i[3],
                                         "territory_ru": i[-3], "territory_ky": i[-2], "territory_en": i[-1]})
                        else:
                            data.append({'culture_name_ru': i[0], 'culture_name_ky': i[1], "culture_name_en": i[2],
                                         'area_ha': i[3], 'productivity': i[4] * i[3],
                                         "territory_ru": 'Кыргызстан', "territory_ky": 'Кыргызстан',
                                         "territory_en": 'Kyrgyzstan'})
                    return Response(data)
        else:
            return Response(data={"message": "parameter 'year or land_type' is required"}, status=400)
