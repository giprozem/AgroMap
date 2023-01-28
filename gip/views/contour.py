from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.views import APIView

from gip.models.contour import Contour, LandType
from gip.pagination.contour_pagination import ContourPagination
from gip.serializers.contour import ContourSerializer, LandTypeSerializer


class LandTypeViewSet(viewsets.ModelViewSet):
    queryset = LandType.objects.all()
    serializer_class = LandTypeSerializer


class ContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ink', 'conton']
    pagination_class = ContourPagination


class FilterContourAPIView(APIView):

    def get(self, request, *args, **kwargs):
        region = request.GET.get('region')
        land_type = request.GET.get('land_type')
        culture = request.GET.get('culture')
        if region and land_type and culture:
            with connection.cursor() as cursor:
                cursor.execute(
                f""" select * from (
                select cntr.id, cntr.ink, cntr.type_id, St_AsGeoJSON(cntr.polygon) as polygon, 
                rank() over (PARTITION BY cntr.id ORDER BY cy.year DESC) AS culture_rank, cl.name, area_ha
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
                where rgn.id in ({region}) and cntr.type_id={land_type} and (cl.id in ({culture}) or cl.id is null)
                order by cntr.id) as temp
                where culture_rank=1;""")
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature",
                                 "properties": {'id': i[0], 'ink': i[1], 'type': i[2],
                                                "culture": i[-2], 'area_ha': i[-1]},
                                 "geometry": eval(i[3])})
                return Response({"type": "FeatureCollection", "features": data})
        elif region and land_type:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                select cntr.id, cntr.ink, cntr.type_id, St_AsGeoJSON(cntr.polygon) as polygon, area_ha 
                                from gip_contour as cntr 
                                join gip_conton as cntn 
                                on cntn.id=cntr.conton_id 
                                join gip_district as dst 
                                on dst.id=cntn.district_id 
                                join gip_region as rgn 
                                on rgn.id=dst.region_id 
                                join gip_landtype as ltp
                                on ltp.id=cntr.type_id
                                where rgn.id in ({region}) and ltp.id={land_type};
                                """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature",
                                 "properties": {'id': i[0], 'ink': i[1], 'type': i[2], 'area_ha': i[-1]},
                                 "geometry": eval(i[3])})
                return Response({"type": "FeatureCollection", "features": data})
        elif region:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               select cntr.id, cntr.ink, cntr.type_id, St_AsGeoJSON(cntr.polygon) as polygon, area_ha
                               from gip_contour as cntr
                               join gip_conton as cntn
                               on cntn.id=cntr.conton_id
                               join gip_district as dst
                               on dst.id=cntn.district_id
                               join gip_region as rgn
                               on rgn.id=dst.region_id
                               where rgn.id in ({region})
                               """)
                rows = cursor.fetchall()
                data = []
                for i in rows:
                    data.append({"type": "Feature",
                                 "properties": {'id': i[0], 'ink': i[1], 'type': i[2], 'area_ha': i[-1]},
                                 "geometry": eval(i[3])})
                return Response({"type": "FeatureCollection", "features": data})
        else:
            return Response(data={"message": "parameter 'region' is required"}, status=400)


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
