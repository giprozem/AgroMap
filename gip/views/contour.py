from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.views import APIView

from gip.models.contour import Contour
from gip.pagination.contour_pagination import ContourPagination
from gip.serializers.contour import ContoursSerializer, ContourSerializer


class ContoursViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContoursSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ink', 'conton']


class ContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ink', 'conton']
    pagination_class = ContourPagination


class FilterContourAPIView(APIView):

    def get(self, request):
        region = request.GET.get('region')
        print(region)
        if region:
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
                print(len(data))
                return Response({"type": "FeatureCollection", "features": data})

