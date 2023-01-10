from rest_framework import viewsets

from hub.models import LandInfo
from hub.serializers.land_info import LandInfoSerializers


class LandInfoViewSet(viewsets.ModelViewSet):
    queryset = LandInfo.objects.all()
    serializer_class = LandInfoSerializers
    lookup_field = 'ink_code'


# class InfoPlotViewSet(viewsets.ModelViewSet):
#     queryset = LandInfo.objects.all()
#     serializer_class = InfoPlotSerializers
#     lookup_field = 'ink_code'
