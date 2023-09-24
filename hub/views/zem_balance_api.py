"""
zem_balance_api.py:
This module handles operations related to land balance.

Classes:
- `ZemBalanceViewSet`: Provides CRUD operations and additional functionalities for `LandInfo` objects related to land balance.
    Attributes:
        - `queryset`: Retrieves all the `LandInfo` objects.
        - `serializer_class`: Serializer used to handle `LandInfo` instances.
        - `permission_classes`: Specifies that users must be authenticated to access this view.
        - `lookup_field`: The field used to look up a `LandInfo` object.

    Methods:
        - `create`: Overridden to process POST requests. Validates if the given land area overlaps with existing ones
          and checks if the `ink_code` is unique.
        - `update`: Overridden to process PUT requests. Updates the given land info object.

- `AsrEniCodeAPIView`: Fetches land details from an external service based on the provided ENI code.
    Methods:
        - `get`: Processes GET requests. It retrieves the details of a land area based on its ENI code.

Note:
For each class or method, the attributes or fields are briefly described with the `#` sign.
"""

import requests
from decouple import config
from django.contrib.gis.geos import GEOSGeometry
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet

from hub.models import LandInfo
from hub.serializers.land_info import ZemBalanceSerializers
from hub.views.handbook_asr import propform, proptype, propforuse, propfor, propstatus


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
            return Response({"Код ошибки": "002",
                             "Пересекается поля с таким ИНК": f"{overlap.values('ink_code')[0].get('ink_code')}"})
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


class AsrEniCodeAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='do not required for front'
    )
    def get(self, request, *args, **kwargs):
        ASR_URL = config("ASR_URL")  # External service URL from config
        eni_code = request.GET.get('eni_code')  # Retrieve ENI code from request
        get_asr = requests.get(f"{ASR_URL}={eni_code}")
        if eni_code and get_asr.text not in 'NULL':
            get_asr_json = get_asr.json()
            data = {'propcode': get_asr_json[0]['propcode'], 'propform': propform.get(get_asr_json[0]['propform']),
                    'proptype': proptype.get(get_asr_json[0]['proptype']),
                    'propforuse': propforuse.get(get_asr_json[0]['propforuse']),
                    'propfor': propfor.get(get_asr_json[0]['propfor']),
                    'propstatus': propstatus.get(get_asr_json[0]['propstatus']),
                    'real_area': get_asr_json[0]['real_area'], 'legl_area': get_asr_json[0]['legl_area'],
                    'ate_name': get_asr_json[0]['ate_name'], 'ate_type_name': get_asr_json[0]['ate_type_name'],
                    'ate2_name': get_asr_json[0]['ate2_name'], 'ate2_type_name': get_asr_json[0]['ate2_type_name'],
                    'ate3_name': get_asr_json[0]['ate3_name'], 'ate3_type_name': get_asr_json[0]['ate3_type_name'],
                    'street_name': get_asr_json[0]['street_name'],
                    'street_type_name': get_asr_json[0]['street_type_name'],
                    'building': get_asr_json[0]['building'], 'flat': get_asr_json[0]['flat'],
                    'uchnum': get_asr_json[0]['uchnum']}
            return Response(data)
        else:
            return Response('NULL')
