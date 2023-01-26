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
