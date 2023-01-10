import requests
from django.contrib.gis.geos import GEOSGeometry, fromstr, Polygon, MultiPolygon
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins, status
from rest_framework.viewsets import GenericViewSet

from hub.models import LandInfo
from hub.serializers.land_info import ZemBalanceSerializers

headers = {
    "token": "p4qfbyzc7eeybt5uq4b2vafc24c386q9"
}


class InkZemBalanceAPIView(APIView):
    def get(self, request):
        ink = request.GET.get('ink')
        if ink:
            url = requests.get(f"https://balance.24mycrm.com/api.php?inkCode={ink}", headers=headers).json()
            # ink_code = url[0]['ink_code']
            # contour = url[0]['main_map']
            # eni = url[0]['eni_code']
            # inn_pin = url[0]['ink_code']
            # name = url[0]['ink_code']
            # bonitet = url[0]['ink_code']
            # culture = url[0]['ink_code']
            # crop_yield = url[0]['ink_code']
            # property_type = url[0]['ink_code']
            # document_type = url[0]['ink_code']
            # document_link = url[0]['ink_code']
            # category_type = url[0]['ink_code']
            # land_type = url[0]['ink_code']
            # square = url[0]['square']
            # return Response([{"ink_code": ink_code, "contour": contour, "eni": eni, "square": square}])
            return Response(url)


class ZemBalanceViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, GenericViewSet):
    queryset = LandInfo.objects.all()
    serializer_class = ZemBalanceSerializers
    permission_classes = [IsAuthenticated]
    lookup_field = 'ink_code'

    def create(self, request, *args, **kwargs):
        coordinates = []
        for i in eval(request.data['main_map'])[0]['coordinates'][0]:
            l = []
            for j in i:
                l.append(float(j))
            coordinates.append(l)
        convert_to_geojson = "{" + f""""type": "{eval(request.data['main_map'])[0]['type']}", "coordinates": [{coordinates}]""" + "}"
        main_map = GEOSGeometry(convert_to_geojson)
        overlap = LandInfo.objects.filter(main_map__intersects=main_map)
        unique_ink_code = LandInfo.objects.filter(ink_code=request.data['ink_code'])
        if unique_ink_code:
            return Response({"Код ошибки - 001": "С таким ИНК в базе существует"})
        if overlap:
            return Response({"Код ошибки": "002", "Пересекается поля с таким ИНК": f"{overlap.values('ink_code')[0].get('ink_code')}"})
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.initial_data['main_map'] = main_map
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        coordinates = []
        for i in eval(request.data['main_map'])[0]['coordinates'][0]:
            l = []
            for j in i:
                l.append(float(j))
            coordinates.append(l)
        convert_to_geojson = "{" + f""""type": "{eval(request.data['main_map'])[0]['type']}", "coordinates": [{coordinates}]""" + "}"
        main_map = GEOSGeometry(convert_to_geojson)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.initial_data['main_map'] = main_map
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)