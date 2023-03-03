from rest_framework import viewsets

from gip.models import Region
from gip.serializers.region import RegionSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
