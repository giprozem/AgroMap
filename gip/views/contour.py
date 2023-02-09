from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from rest_framework import viewsets, filters
from rest_framework.views import APIView

from gip.models.contour import Contour, LandType, ContourYear
from gip.pagination.contour_pagination import ContourPagination, SearchContourPagination
from gip.serializers.contour import ContourSerializer, LandTypeSerializer, ContourYearSerializer


class LandTypeViewSet(viewsets.ModelViewSet):
    queryset = LandType.objects.all()
    serializer_class = LandTypeSerializer


class ContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ink', 'conton']
    pagination_class = ContourPagination


class ContourYearViewSet(viewsets.ModelViewSet):
    queryset = ContourYear.objects.all()
    serializer_class = ContourYearSerializer
    pagination_class = ContourPagination


class SearchContourViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ink', 'conton']
    pagination_class = SearchContourPagination


class FilterContourAPIView(APIView):

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
                               gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, St_AsGeoJSON(gcy.polygon) as polygon  
                               FROM gip_contour AS cntr 
                               INNER JOIN gip_contouryear_contour AS cyc ON cntr.id=cyc.contour_id 
                               INNER JOIN gip_contouryear AS gcy ON gcy.id=cyc.contouryear_id
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
                                                                "properties": {'contour_id': i[0],  'contour_cs': i[4],
                                                                               'contour_year_id': i[1],
                                                                               'land_type_id': i[2],
                                                                               'contour_year_cs': i[5],
                                                                               'year': i[6], 'ink': i[3], 'area_ha': i[7]},
                                                                "geometry": eval(i[-1])}]}})
                return Response(data)
        elif region and district and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                                gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, St_AsGeoJSON(gcy.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                INNER JOIN gip_contouryear_contour AS cyc ON cntr.id=cyc.contour_id 
                                INNER JOIN gip_contouryear AS gcy ON gcy.id=cyc.contouryear_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where gcy.type_id in ({land_type}) and rgn.id in ({region}) and gcy.year='{year}'
                                and dst.id=({district}) order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                                 "contour_year": {"type": "FeatureCollection",
                                                  "features": [{"type": "Feature",
                                                                "properties": {'contour_id': i[0],  'contour_cs': i[4],
                                                                               'contour_year_id': i[1],
                                                                               'land_type_id': i[2],
                                                                               'contour_year_cs': i[5],
                                                                               'year': i[6], 'ink': i[3], 'area_ha': i[7]},
                                                                "geometry": eval(i[-1])}]}})
                return Response(data)
        elif region and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                                gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, St_AsGeoJSON(gcy.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                INNER JOIN gip_contouryear_contour AS cyc ON cntr.id=cyc.contour_id 
                                INNER JOIN gip_contouryear AS gcy ON gcy.id=cyc.contouryear_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where  gcy.type_id in ({land_type}) and rgn.id in ({region}) and gcy.year='{year}'
                                order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                                 "contour_year": {"type": "FeatureCollection",
                                                  "features": [{"type": "Feature",
                                                                "properties": {'contour_id': i[0],  'contour_cs': i[4],
                                                                               'contour_year_id': i[1],
                                                                               'land_type_id': i[2],
                                                                               'contour_year_cs': i[5],
                                                                               'year': i[6], 'ink': i[3], 'area_ha': i[7]},
                                                                "geometry": eval(i[-1])}]}})
                return Response(data)
        elif year:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                SELECT cntr.id AS contour_id, gcy.id AS contour_year_id, 
                                gcy.type_id AS land_type_id, cntr.ink, cntr.code_soato AS contour_cs,
                                gcy.code_soato AS contour_year_cs, gcy.year, gcy.area_ha, St_AsGeoJSON(gcy.polygon) as polygon  
                                FROM gip_contour AS cntr 
                                INNER JOIN gip_contouryear_contour AS cyc ON cntr.id=cyc.contour_id 
                                INNER JOIN gip_contouryear AS gcy ON gcy.id=cyc.contouryear_id
                                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                                JOIN gip_district AS dst ON dst.id=cntn.district_id
                                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                                where gcy.year='{year}'
                                order by cntr.id;
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({
                                 "contour_year": {"type": "FeatureCollection",
                                                  "features": [{"type": "Feature",
                                                                "properties": {'contour_id': i[0],  'contour_cs': i[4],
                                                                               'contour_year_id': i[1],
                                                                               'land_type_id': i[2],
                                                                               'contour_year_cs': i[5],
                                                                               'year': i[6], 'ink': i[3], 'area_ha': i[7]},
                                                                "geometry": eval(i[-1])}]}})
                return Response(data)
        else:
            return Response(data={"message": "parameter 'year or land_type' is required"}, status=400)


class PastureClassAPIView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT
                    cntr.id, cntr.ink, cntr.type_id,
                    St_AsGeoJSON(cntr.polygon) as polygon,
                    cntr.area_ha,
                    cai.value
                FROM gip_contour as cntr
                JOIN indexes_contouraverageindex as cai
                ON cntr.id = cai.contour_id
                WHERE cntr.type_id = 2
                ORDER BY cai.value DESC
            """)
            rows = cursor.fetchall()
        data = {}
        prod_classes = ["high", "middle", "low"]
        # print(rows[:3])
        for num, cl in enumerate(prod_classes):
            data[cl] = {"type": "FeatureCollection", "features": []}
            start = round(num*len(rows)/len(prod_classes))
            end = round((num+1)*len(rows)/len(prod_classes))
            for i in rows[start:end]:
                data[cl]["features"].append({"type": "Feature",
                            "properties": {'id': i[0], 'ink': i[1], 'type': i[2], 'avg_index': i[-1]},
                             "geometry": eval(i[3])
                            })

        return Response(data)


class ContourSearchAPIView(ListAPIView):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
    pagination_class = SearchContourPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['ink']


class ContourStatisticsAPIView(APIView):
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
    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        year = request.GET.get('year')
        land_type = request.GET.get('land_type')
        district = request.GET.get('district')
        if region and district and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f""" select 
                round(sum(case when (gcy.productivity)::float > 1.6 then gcy.area_ha else 0 end)) as "Productive", 
                round(sum(case when (gcy.productivity)::float <= 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                cntn.name from  gip_contour AS cntr 
                INNER JOIN gip_contouryear_contour AS cyc ON cntr.id=cyc.contour_id 
                INNER JOIN gip_contouryear AS gcy ON gcy.id=cyc.contouryear_id
                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                JOIN gip_district AS dst ON dst.id=cntn.district_id
                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                where rgn.id in ({region}) and gcy.type_id=2 and gcy.year='{year}' and dst.id in ({district})
                group by cntn.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'Conton': i[2], 'Productive': i[0], 'Unproductive': i[1]})
                return Response(data)
        elif region and land_type and year:
            with connection.cursor() as cursor:
                cursor.execute(f""" select 
                round(sum(case when (gcy.productivity)::float > 1.6 then gcy.area_ha else 0 end)) as "Productive", 
                round(sum(case when (gcy.productivity)::float <= 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                dst.name from  gip_contour AS cntr 
                INNER JOIN gip_contouryear_contour AS cyc ON cntr.id=cyc.contour_id 
                INNER JOIN gip_contouryear AS gcy ON gcy.id=cyc.contouryear_id
                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                JOIN gip_district AS dst ON dst.id=cntn.district_id
                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                where rgn.id in ({region}) and gcy.type_id=2 and gcy.year='{year}'
                group by dst.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'District': i[2], 'Productive': i[0], 'Unproductive': i[1]})
                return Response(data)
        elif year:
            with connection.cursor() as cursor:
                cursor.execute(f"""select 
                round(sum(case when (gcy.productivity)::float > 1.6 then gcy.area_ha else 0 end)) as "Productive", 
                round(sum(case when (gcy.productivity)::float <= 1.6 then gcy.area_ha else 0 end)) as "Unproductive",
                rgn.name from  gip_contour AS cntr 
                INNER JOIN gip_contouryear_contour AS cyc ON cntr.id=cyc.contour_id 
                INNER JOIN gip_contouryear AS gcy ON gcy.id=cyc.contouryear_id
                JOIN gip_conton AS cntn ON cntn.id=cntr.conton_id
                JOIN gip_district AS dst ON dst.id=cntn.district_id
                JOIN gip_region AS rgn ON rgn.id=dst.region_id
                where gcy.year='{year}' and gcy.type_id=2
                group by rgn.name;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({'Region': i[2], 'Productive': i[0], 'Unproductive': i[1]})
                return Response(data)
