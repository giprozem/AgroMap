import requests
from decouple import config
from django.contrib.gis.geos import GEOSGeometry
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
    def get(self, request, *args, **kwargs):
        ASR_URL = config("ASR_URL")
        eni_code = request.GET.get('eni_code')
        get_asr = requests.get(f"{ASR_URL}={eni_code}")
        if eni_code and get_asr.text not in 'NULL':
            get_asr_json = get_asr.json()
            LandInfo.objects.update_or_create(defaults={'eni_code': get_asr_json[0]['propcode']},
                                              propform=propform.get(get_asr_json[0]['propform']),
                                              proptype=proptype.get(get_asr_json[0]['proptype']),
                                              propforuse=propforuse.get(get_asr_json[0]['propforuse']),
                                              propfor=propfor.get(get_asr_json[0]['propfor']),
                                              propstatus=propstatus.get(
                                                  get_asr_json[0]['propstatus']),
                                              real_area=get_asr_json[0]['real_area'],
                                              legl_area=get_asr_json[0]['legl_area'],
                                              ate_name=get_asr_json[0]['ate_name'],
                                              ate_type_name=get_asr_json[0]['ate_type_name'],
                                              ate2_name=get_asr_json[0]['ate2_name'],
                                              ate2_type_name=get_asr_json[0]['ate2_type_name'],
                                              ate3_name=get_asr_json[0]['ate3_name'],
                                              ate3_type_name=get_asr_json[0]['ate3_type_name'],
                                              street_name=get_asr_json[0]['street_name'],
                                              street_type_name=get_asr_json[0]['street_type_name'],
                                              building=get_asr_json[0]['building'], flat=get_asr_json[0]['flat'],
                                              uchnum=get_asr_json[0]['uchnum'])
            a = LandInfo.objects.filter(eni_code=eni_code)
            data = []
            for i in a:
                data.append({'propcode': i.eni_code, 'propform': i.propform,
                             'proptype': i.proptype,
                             'propforuse': i.propforuse,
                             'propfor': i.propfor,
                             'propstatus': i.propstatus,
                             'real_area': i.real_area, 'legl_area': i.legl_area,
                             'ate_name': i.ate_name, 'ate_type_name': i.ate_type_name,
                             'ate2_name': i.ate2_name, 'ate2_type_name': i.ate2_type_name,
                             'ate3_name': i.ate3_name, 'ate3_type_name': i.ate3_type_name,
                             'street_name': i.street_name,
                             'street_type_name': i.street_type_name,
                             'building': i.building, 'flat': i.flat,
                             'uchnum': i.uchnum})
            return Response(data)
        else:
            return Response('NULL')
