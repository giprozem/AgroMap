from django.contrib.gis.geos import Point, Polygon
from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import Conton, District
from gip.models.contour import Contour
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


class OccurrenceCheckAPIView(APIView):
    def get(self, request, *args, **kwargs):
        point = request.GET.get('point')
        polygon = request.GET.get('polygon')

        if point:
            points = Point(eval(point))
            with connection.cursor() as cursor:
                cursor.execute(f"""
                               select rgn.name as region_name,  dst.name as district_name, cntn.name as conton_name 
                               from gip_district as dst join gip_region as rgn
                               on rgn.id = dst.region_id
                               join gip_conton as cntn
                               on dst.id = cntn.district_id 
                               where ST_Contains(cntn.polygon::geometry, '{points}'::geography::geometry);
                               """)
                rows = cursor.fetchall()
                data = {
                    'region': f"{[row[0] for row in rows]}".strip("['']"),
                    'district': f"{[row[1] for row in rows]}".strip("['']"),
                    'conton': f"{[row[-1] for row in rows]}".strip("['']")
                }
                return Response(data)
        elif polygon:
            polygons = Polygon(eval(polygon))
            with connection.cursor() as cursor:
                cursor.execute(f"""
                                          select rgn.name as region_name,  dst.name as district_name, cntn.name as conton_name 
                                          from gip_district as dst join gip_region as rgn
                                          on rgn.id = dst.region_id
                                          join gip_conton as cntn
                                          on dst.id = cntn.district_id 
                                          where ST_Contains(cntn.polygon::geometry, '{polygons}'::geography::geometry);
                                          """)
                rows = cursor.fetchall()
                data = {
                    'region': f"{[row[0] for row in rows]}".strip("['']"),
                    'district': f"{[row[1] for row in rows]}".strip("['']"),
                    'conton': f"{[row[-1] for row in rows]}".strip("['']")
                }
                return Response(data)
        else:
            return Response(data={"message": "parameter 'point or polygon' is required"}, status=400)

