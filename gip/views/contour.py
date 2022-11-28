from django.contrib.gis.geos import Point
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from gip.models import Conton, District
from gip.models.contour import Contour
from gip.serializers.contour import ContourSerializer


class ContourViewSet(viewsets.ModelViewSet):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer

    # def get_queryset(self):
    #     return self.queryset.filter(created_by=self.request.user)


class PointAPIView(APIView):
    def get(self, request, *args, **kwargs):
        latlong = request.GET.get('latlong')
        if latlong:
            point = Point(eval(latlong))
            contons = Conton.objects.filter(polygon__contains=point)
            district = District.objects.filter(polygon__contains=point)
            return Response({"Conton": f"{contons[0].name}",
                             "District": f"{district[0].name}",
                             "Region": f"{district[0].region}"})
        else:
            return Response('/get_contour?latlong=74.61313199999999,42.832171')
